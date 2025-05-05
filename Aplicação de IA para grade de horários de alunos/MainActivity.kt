package com.example.geradorgrade.ui.activity

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
// Import necessary components like BottomNavigationView, NavHostFragment etc.
// Import ViewBinding

class MainActivity : AppCompatActivity() {

    // private lateinit var binding: ActivityMainBinding // ViewBinding
    // private lateinit var viewModel: MainViewModel // ViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // binding = ActivityMainBinding.inflate(layoutInflater)
        // setContentView(binding.root)

        // Setup ViewModel
        // viewModel = ViewModelProvider(this).get(MainViewModel::class.java)

        // Setup BottomNavigationView with NavController
        // val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        // val navController = navHostFragment.navController
        // binding.bottomNavigationView.setupWithNavController(navController)

        // Initial session creation call (example)
        // viewModel.createSession()

        // Observe ViewModel LiveData (e.g., session ID, errors)
        // viewModel.sessionId.observe(this, Observer { sessionId -> ... })
        // viewModel.error.observe(this, Observer { error -> ... })

        println("MainActivity created - Placeholder") // Placeholder log
    }
}

