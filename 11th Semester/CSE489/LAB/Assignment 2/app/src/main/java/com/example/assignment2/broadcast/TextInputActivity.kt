package com.example.assignment2.broadcast

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.assignment2.databinding.ActivityTextInputBinding

class TextInputActivity : AppCompatActivity() {

    private lateinit var binding: ActivityTextInputBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityTextInputBinding.inflate(layoutInflater)
        setContentView(binding.root)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        binding.btnSend.setOnClickListener {
            val message = binding.editMessage.text?.toString()?.trim().orEmpty()
            if (message.isEmpty()) {
                binding.inputLayout.error = getString(com.example.assignment2.R.string.error_empty_message)
                return@setOnClickListener
            }
            binding.inputLayout.error = null

            val intent = Intent(this, CustomReceiverActivity::class.java)
                .putExtra(CustomReceiverActivity.EXTRA_MESSAGE, message)
            startActivity(intent)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
