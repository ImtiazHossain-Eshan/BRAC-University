package com.example.assignment2.ui.image

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.view.isVisible
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.assignment2.databinding.FragmentImageScaleBinding

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
        private const val IMAGE_URL = "https://images2.minutemediacdn.com/image/upload/images/voltaxMediaLibrary/mmsport/si/01kvjnfhrs4wnppd2r2h.jpg"
        private const val LOADING_TIMEOUT_MS = 10_000L
    }
}
