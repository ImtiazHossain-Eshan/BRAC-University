package com.example.assignment2

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.example.assignment2.databinding.ActivityMainBinding

/**
 * Hosts the navigation drawer (Jetpack Navigation component) and swaps between the four
 * drawer destinations: Broadcast Receiver, Image Scale, Video and Audio.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.appBarMain.toolbar)

        // With FragmentContainerView the NavHostFragment is created by the FragmentManager, so the
        // NavController must be obtained from the host fragment rather than findNavController(viewId),
        // which is not yet available in onCreate().
        val navController = navHostFragment().navController

        // Every drawer entry is a top-level destination, so each shows the hamburger icon.
        appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.nav_broadcast,
                R.id.nav_image,
                R.id.nav_video,
                R.id.nav_audio
            ),
            binding.drawerLayout
        )
        setupActionBarWithNavController(navController, appBarConfiguration)
        binding.navView.setupWithNavController(navController)
    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = navHostFragment().navController
        return navController.navigateUp(appBarConfiguration) || super.onSupportNavigateUp()
    }

    private fun navHostFragment(): NavHostFragment =
        supportFragmentManager.findFragmentById(R.id.nav_host_fragment_content_main) as NavHostFragment
}
