package com.example.assignment2.ui.audio

import android.media.MediaPlayer
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.SeekBar
import androidx.fragment.app.Fragment
import com.example.assignment2.R
import com.example.assignment2.databinding.FragmentAudioBinding

/**
 * D. Audio.
 *
 * Plays a bundled audio file inside the app using [MediaPlayer], with play/pause and stop controls
 * and a seek bar that tracks the playback position.
 */
class AudioFragment : Fragment() {

    private var _binding: FragmentAudioBinding? = null
    private val binding get() = _binding!!

    private var mediaPlayer: MediaPlayer? = null
    private val handler = Handler(Looper.getMainLooper())

    private val updateProgress = object : Runnable {
        override fun run() {
            val player = mediaPlayer ?: return
            val b = _binding ?: return
            val position = player.currentPosition
            b.seekBar.progress = position
            b.textTime.text = timeLabel(position, player.duration)
            handler.postDelayed(this, PROGRESS_INTERVAL_MS)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentAudioBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val player = MediaPlayer.create(requireContext(), R.raw.sample_audio)
        if (player == null) {
            binding.textAudioTitle.text = getString(R.string.audio_error)
            binding.btnPlayPause.isEnabled = false
            binding.btnStop.isEnabled = false
            return
        }
        mediaPlayer = player

        binding.seekBar.max = player.duration
        binding.textTime.text = timeLabel(0, player.duration)

        binding.btnPlayPause.setOnClickListener {
            val mp = mediaPlayer ?: return@setOnClickListener
            if (mp.isPlaying) {
                mp.pause()
                binding.btnPlayPause.text = getString(R.string.play)
                handler.removeCallbacks(updateProgress)
            } else {
                mp.start()
                binding.btnPlayPause.text = getString(R.string.pause)
                handler.post(updateProgress)
            }
        }

        binding.btnStop.setOnClickListener {
            val mp = mediaPlayer ?: return@setOnClickListener
            mp.pause()
            mp.seekTo(0)
            binding.seekBar.progress = 0
            binding.textTime.text = timeLabel(0, mp.duration)
            binding.btnPlayPause.text = getString(R.string.play)
            handler.removeCallbacks(updateProgress)
        }

        player.setOnCompletionListener {
            it.seekTo(0)
            binding.seekBar.progress = 0
            binding.textTime.text = timeLabel(0, it.duration)
            binding.btnPlayPause.text = getString(R.string.play)
            handler.removeCallbacks(updateProgress)
        }

        binding.seekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                if (fromUser) {
                    mediaPlayer?.seekTo(progress)
                    binding.textTime.text = timeLabel(progress, mediaPlayer?.duration ?: 0)
                }
            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })
    }

    override fun onPause() {
        super.onPause()
        val mp = mediaPlayer ?: return
        if (mp.isPlaying) {
            mp.pause()
            binding.btnPlayPause.text = getString(R.string.play)
            handler.removeCallbacks(updateProgress)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        handler.removeCallbacks(updateProgress)
        mediaPlayer?.release()
        mediaPlayer = null
        _binding = null
    }

    private fun timeLabel(positionMs: Int, durationMs: Int): String =
        "${formatTime(positionMs)} / ${formatTime(durationMs)}"

    private fun formatTime(ms: Int): String {
        val totalSeconds = ms / 1000
        return "%02d:%02d".format(totalSeconds / 60, totalSeconds % 60)
    }

    companion object {
        private const val PROGRESS_INTERVAL_MS = 500L
    }
}
