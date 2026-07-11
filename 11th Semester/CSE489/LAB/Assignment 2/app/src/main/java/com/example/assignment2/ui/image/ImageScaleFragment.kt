package com.example.assignment2.ui.image

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.view.isVisible
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.assignment2.databinding.FragmentImageScaleBinding

/**
 * B. Image scale.
 *
 * Loads an image from the internet with Glide into a [ZoomableImageView], which the user can then
 * scale with a pinch gesture (and pan / double-tap to reset).
 */
class ImageScaleFragment : Fragment() {

    private var _binding: FragmentImageScaleBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentImageScaleBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.progressImage.isVisible = true

        // Hide the spinner as soon as Glide sets the loaded image on the view.
        binding.imageView.onDrawableSet = {
            _binding?.progressImage?.isVisible = false
        }
        // Safety net: never leave the spinner running if the network stalls.
        binding.imageView.postDelayed({
            _binding?.progressImage?.isVisible = false
        }, LOADING_TIMEOUT_MS)

        Glide.with(this)
            .load(IMAGE_URL)
            .into(binding.imageView)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        // A fixed, freely usable photo from Lorem Picsum (loaded from the internet).
        private const val IMAGE_URL = "https://picsum.photos/id/1015/1080/1440"
        private const val LOADING_TIMEOUT_MS = 10_000L
    }
}
