package com.example.assignment2.ui.image

import android.content.Context
import android.graphics.Matrix
import android.graphics.PointF
import android.graphics.drawable.Drawable
import android.util.AttributeSet
import android.view.GestureDetector
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import androidx.appcompat.widget.AppCompatImageView

/**
 * B. Image scale.
 *
 * An [AppCompatImageView] that supports pinch-to-zoom (and drag-to-pan once zoomed in) by driving
 * an image [Matrix] from a [ScaleGestureDetector]. Double-tap resets the image back to fit.
 *
 * The base "fit to screen" transform is recomputed whenever a new drawable is supplied (for example
 * when Glide finishes loading the image from the internet) or when the view is (re)measured.
 */
class ZoomableImageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : AppCompatImageView(context, attrs, defStyleAttr) {

    private val touchMatrix = Matrix()
    private val matrixValues = FloatArray(9)

    private val minScale = 1f
    private val maxScale = 5f
    private var saveScale = 1f

    // Size of the image after the initial fit-to-screen scale (at saveScale == 1).
    private var fittedWidth = 0f
    private var fittedHeight = 0f

    private var viewWidth = 0
    private var viewHeight = 0

    private var mode = NONE
    private val last = PointF()

    /** Invoked whenever a non-null drawable is set (e.g. after Glide finishes loading). */
    var onDrawableSet: (() -> Unit)? = null

    private val scaleDetector = ScaleGestureDetector(context, ScaleListener())
    private val gestureDetector =
        GestureDetector(context, object : GestureDetector.SimpleOnGestureListener() {
            override fun onDoubleTap(e: MotionEvent): Boolean {
                fitToScreen()
                return true
            }
        })

    init {
        super.setClickable(true)
        scaleType = ScaleType.MATRIX
        imageMatrix = touchMatrix
    }

    override fun setImageDrawable(drawable: Drawable?) {
        super.setImageDrawable(drawable)
        // A new image was set (e.g. by Glide). Fit it once the view has valid dimensions.
        if (viewWidth > 0 && viewHeight > 0) {
            fitToScreen()
        } else {
            post { fitToScreen() }
        }
        if (drawable != null) {
            onDrawableSet?.invoke()
        }
    }

    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec)
        val newWidth = MeasureSpec.getSize(widthMeasureSpec)
        val newHeight = MeasureSpec.getSize(heightMeasureSpec)
        if (newWidth != viewWidth || newHeight != viewHeight) {
            viewWidth = newWidth
            viewHeight = newHeight
            fitToScreen()
        }
    }

    private fun fitToScreen() {
        val d = drawable ?: return
        if (d.intrinsicWidth == 0 || d.intrinsicHeight == 0) return
        if (viewWidth == 0 || viewHeight == 0) return

        saveScale = 1f
        val scale = minOf(
            viewWidth.toFloat() / d.intrinsicWidth,
            viewHeight.toFloat() / d.intrinsicHeight
        )
        touchMatrix.setScale(scale, scale)

        val redundantX = (viewWidth - scale * d.intrinsicWidth) / 2f
        val redundantY = (viewHeight - scale * d.intrinsicHeight) / 2f
        touchMatrix.postTranslate(redundantX, redundantY)

        fittedWidth = viewWidth - 2 * redundantX
        fittedHeight = viewHeight - 2 * redundantY
        imageMatrix = touchMatrix
    }

    override fun performClick(): Boolean {
        super.performClick()
        return true
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        scaleDetector.onTouchEvent(event)
        gestureDetector.onTouchEvent(event)

        val point = PointF(event.x, event.y)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN -> {
                last.set(point)
                mode = DRAG
            }

            MotionEvent.ACTION_MOVE -> if (mode == DRAG) {
                val dx = getFixedDrag(point.x - last.x, viewWidth.toFloat(), fittedWidth * saveScale)
                val dy = getFixedDrag(point.y - last.y, viewHeight.toFloat(), fittedHeight * saveScale)
                touchMatrix.postTranslate(dx, dy)
                clampTranslation()
                last.set(point)
                imageMatrix = touchMatrix
            }

            MotionEvent.ACTION_POINTER_DOWN -> {
                last.set(point)
                mode = ZOOM
            }

            MotionEvent.ACTION_UP, MotionEvent.ACTION_POINTER_UP -> mode = NONE
        }
        return true
    }

    private inner class ScaleListener : ScaleGestureDetector.SimpleOnScaleGestureListener() {
        override fun onScaleBegin(detector: ScaleGestureDetector): Boolean {
            mode = ZOOM
            return true
        }

        override fun onScale(detector: ScaleGestureDetector): Boolean {
            var scaleFactor = detector.scaleFactor
            val previous = saveScale
            saveScale *= scaleFactor
            when {
                saveScale > maxScale -> {
                    saveScale = maxScale
                    scaleFactor = maxScale / previous
                }

                saveScale < minScale -> {
                    saveScale = minScale
                    scaleFactor = minScale / previous
                }
            }

            if (fittedWidth * saveScale <= viewWidth || fittedHeight * saveScale <= viewHeight) {
                touchMatrix.postScale(scaleFactor, scaleFactor, viewWidth / 2f, viewHeight / 2f)
            } else {
                touchMatrix.postScale(scaleFactor, scaleFactor, detector.focusX, detector.focusY)
            }
            clampTranslation()
            imageMatrix = touchMatrix
            return true
        }
    }

    /** Keeps the image edges from drifting inside the view. */
    private fun clampTranslation() {
        touchMatrix.getValues(matrixValues)
        val transX = matrixValues[Matrix.MTRANS_X]
        val transY = matrixValues[Matrix.MTRANS_Y]
        val fixX = getFixedTranslation(transX, viewWidth.toFloat(), fittedWidth * saveScale)
        val fixY = getFixedTranslation(transY, viewHeight.toFloat(), fittedHeight * saveScale)
        if (fixX != 0f || fixY != 0f) {
            touchMatrix.postTranslate(fixX, fixY)
        }
    }

    private fun getFixedTranslation(trans: Float, viewSize: Float, contentSize: Float): Float {
        val minTrans: Float
        val maxTrans: Float
        if (contentSize <= viewSize) {
            minTrans = 0f
            maxTrans = viewSize - contentSize
        } else {
            minTrans = viewSize - contentSize
            maxTrans = 0f
        }
        return when {
            trans < minTrans -> minTrans - trans
            trans > maxTrans -> maxTrans - trans
            else -> 0f
        }
    }

    private fun getFixedDrag(delta: Float, viewSize: Float, contentSize: Float): Float {
        // Only allow panning along an axis where the (zoomed) image is larger than the view.
        return if (contentSize <= viewSize) 0f else delta
    }

    companion object {
        private const val NONE = 0
        private const val DRAG = 1
        private const val ZOOM = 2
    }
}
