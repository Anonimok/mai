package com.example.geradorgrade.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
// Import ViewBinding
// Import necessary UI components (TextInputLayout, Button, etc.)
import com.example.geradorgrade.ui.viewmodel.MainViewModel

class PreferencesFragment : Fragment() {

    // private var _binding: FragmentPreferencesBinding? = null
    // private val binding get() = _binding!!
    private val viewModel: MainViewModel by activityViewModels() // Shared ViewModel

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // _binding = FragmentPreferencesBinding.inflate(inflater, container, false)
        // return binding.root
        println("PreferencesFragment created - Placeholder View") // Placeholder log
        return View(context) // Return a dummy view for now
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Setup UI listeners (e.g., button click for saving preferences)
        // binding.buttonSavePreferences.setOnClickListener { savePreferences() }

        // Observe ViewModel LiveData (e.g., session ID, save status, errors)
        // viewModel.sessionId.observe(viewLifecycleOwner) { sessionId -> ... }
        // viewModel.preferencesSaveStatus.observe(viewLifecycleOwner) { status -> showSaveFeedback(status) }
        // viewModel.error.observe(viewLifecycleOwner) { error -> showError(error) }
    }

    // private fun savePreferences() {
    //    val minCredits = binding.editTextMinCredits.text.toString().toIntOrNull()
    //    val maxCredits = binding.editTextMaxCredits.text.toString().toIntOrNull()
    //    if (minCredits != null && maxCredits != null) {
    //        viewModel.savePreferences(minCredits, maxCredits)
    //    } else {
    //        // Show validation error
    //    }
    // }

    // private fun showSaveFeedback(status: SaveStatus) { ... }
    // private fun showError(errorMessage: String?) { ... }

    override fun onDestroyView() {
        super.onDestroyView()
        // _binding = null // Clean up binding
    }
}

