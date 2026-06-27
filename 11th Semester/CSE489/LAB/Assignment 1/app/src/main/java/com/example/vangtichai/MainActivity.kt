package com.example.vangtichai

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
class MainActivity : AppCompatActivity() {
    private var entered: String = ""

    private lateinit var tvAmount: TextView
    private lateinit var noteViews: Map<Int, TextView>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvAmount = findViewById(R.id.tvAmount)
        noteViews = mapOf(
            500 to findViewById(R.id.tv500),
            100 to findViewById(R.id.tv100),
            50 to findViewById(R.id.tv50),
            20 to findViewById(R.id.tv20),
            10 to findViewById(R.id.tv10),
            5 to findViewById(R.id.tv5),
            2 to findViewById(R.id.tv2),
            1 to findViewById(R.id.tv1)
        )

        // Wire up the ten digit buttons.
        val digitButtons = listOf(
            R.id.btn0 to 0, R.id.btn1 to 1, R.id.btn2 to 2, R.id.btn3 to 3,
            R.id.btn4 to 4, R.id.btn5 to 5, R.id.btn6 to 6, R.id.btn7 to 7,
            R.id.btn8 to 8, R.id.btn9 to 9
        )
        for ((id, digit) in digitButtons) {
            findViewById<Button>(id).setOnClickListener { onDigit(digit) }
        }
        findViewById<Button>(R.id.btnClear).setOnClickListener { onClear() }

        // Restore the entered amount across configuration changes (e.g. rotation).
        if (savedInstanceState != null) {
            entered = savedInstanceState.getString(KEY_ENTERED, "")
        }
        updateUi()
    }
    private fun onDigit(digit: Int) {
        entered = when {
            entered == "0" -> digit.toString()        // replace a lone leading zero
            entered.length >= MAX_DIGITS -> entered    // cap length, ignore extra input
            else -> entered + digit
        }
        updateUi()
    }

    private fun onClear() {
        entered = ""
        updateUi()
    }
    private fun updateUi() {
        tvAmount.text =
            if (entered.isEmpty()) getString(R.string.taka_label)
            else getString(R.string.taka_amount, entered)

        val amount = if (entered.isEmpty()) 0L else entered.toLong()
        val counts = ChangeCalculator.changeFor(amount)
        for (i in ChangeCalculator.DENOMINATIONS.indices) {
            val note = ChangeCalculator.DENOMINATIONS[i]
            noteViews[note]?.text = getString(R.string.note_row, note, counts[i])
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putString(KEY_ENTERED, entered)
    }

    companion object {
        private const val KEY_ENTERED = "entered_amount"
        private const val MAX_DIGITS = 9
    }
}
