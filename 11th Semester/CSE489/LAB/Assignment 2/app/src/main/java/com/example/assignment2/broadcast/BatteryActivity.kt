package com.example.assignment2.broadcast

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.BatteryManager
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.example.assignment2.R
import com.example.assignment2.databinding.ActivityBatteryBinding

/**
 * A.2 — Second activity for the "System battery notification receiver" option.
 *
 * Registers a receiver for the system broadcast [Intent.ACTION_BATTERY_CHANGED] and shows the
 * current battery percentage and charging state.
 */
class BatteryActivity : AppCompatActivity() {

    private lateinit var binding: ActivityBatteryBinding

    private val batteryReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context, intent: Intent) {
            updateBattery(intent)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityBatteryBinding.inflate(layoutInflater)
        setContentView(binding.root)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
    }

    override fun onStart() {
        super.onStart()
        val filter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)
        // ACTION_BATTERY_CHANGED is sticky: registering returns the latest battery status intent.
        val sticky = ContextCompat.registerReceiver(
            this,
            batteryReceiver,
            filter,
            ContextCompat.RECEIVER_NOT_EXPORTED
        )
        sticky?.let { updateBattery(it) }
    }

    override fun onStop() {
        super.onStop()
        unregisterReceiver(batteryReceiver)
    }

    private fun updateBattery(intent: Intent) {
        val level = intent.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        val scale = intent.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        val percent = if (level >= 0 && scale > 0) level * 100 / scale else -1

        binding.textBatteryPercent.text = if (percent >= 0) {
            getString(R.string.battery_percentage, percent)
        } else {
            getString(R.string.battery_unknown)
        }
        binding.progressBattery.progress = percent.coerceIn(0, 100)

        val status = intent.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        val isCharging = status == BatteryManager.BATTERY_STATUS_CHARGING ||
                status == BatteryManager.BATTERY_STATUS_FULL
        binding.textChargingStatus.text = getString(
            if (isCharging) R.string.battery_charging else R.string.battery_not_charging
        )
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
