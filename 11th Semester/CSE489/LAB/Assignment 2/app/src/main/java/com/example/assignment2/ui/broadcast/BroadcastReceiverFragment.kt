package com.example.assignment2.ui.broadcast

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.fragment.app.Fragment
import com.example.assignment2.R
import com.example.assignment2.broadcast.BatteryActivity
import com.example.assignment2.broadcast.TextInputActivity
import com.example.assignment2.databinding.FragmentBroadcastBinding

/**
 * A. Broadcast Receiver.
 *
 * Shows a spinner where the user selects the type of broadcast operation and a button to proceed
 * to the next activity:
 *   - position 0 -> Custom broadcast receiver  -> [TextInputActivity]
 *   - position 1 -> System battery receiver     -> [BatteryActivity]
 */
class BroadcastReceiverFragment : Fragment() {

    private var _binding: FragmentBroadcastBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentBroadcastBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val adapter = ArrayAdapter.createFromResource(
            requireContext(),
            R.array.broadcast_types,
            android.R.layout.simple_spinner_item
        ).apply {
            setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        }
        binding.spinnerBroadcastType.adapter = adapter

        binding.btnProceed.setOnClickListener {
            when (binding.spinnerBroadcastType.selectedItemPosition) {
                CUSTOM_BROADCAST -> startActivity(
                    Intent(requireContext(), TextInputActivity::class.java)
                )

                BATTERY_BROADCAST -> startActivity(
                    Intent(requireContext(), BatteryActivity::class.java)
                )
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        private const val CUSTOM_BROADCAST = 0
        private const val BATTERY_BROADCAST = 1
    }
}
