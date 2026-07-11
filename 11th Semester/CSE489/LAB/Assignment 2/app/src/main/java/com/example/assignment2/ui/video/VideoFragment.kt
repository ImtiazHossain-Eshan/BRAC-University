package com.example.assignment2.ui.video

import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.MediaController
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.assignment2.R
import com.example.assignment2.databinding.FragmentVideoBinding

/**
 * C. Video.
 *
 * Plays a bundled video inside the app using a [android.widget.VideoView] (backed by MediaPlayer)
 * together with a [MediaController] for play/pause/seek controls.
 */
class VideoFragment : Fragment() {

    private var _binding: FragmentVideoBinding? = null
    private val binding get() = _binding!!

    private var playbackPosition = 0

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentVideoBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val videoUri = Uri.parse(
            "android.resource://${requireContext().packageName}/${R.raw.sample_video}"
        )

        val mediaController = MediaController(requireContext())
        mediaController.setAnchorView(binding.videoView)

        binding.videoView.apply {
            setMediaController(mediaController)
            setVideoURI(videoUri)
            setOnPreparedListener { mp ->
                mp.isLooping = false
                if (playbackPosition > 0) seekTo(playbackPosition)
                start()
            }
            setOnErrorListener { _, _, _ ->
                Toast.makeText(requireContext(), R.string.video_error, Toast.LENGTH_SHORT).show()
                true
            }
        }
    }

    override fun onPause() {
        super.onPause()
        _binding?.videoView?.let {
            if (it.isPlaying) {
                playbackPosition = it.currentPosition
            }
            it.pause()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding?.videoView?.stopPlayback()
        _binding = null
    }
}
