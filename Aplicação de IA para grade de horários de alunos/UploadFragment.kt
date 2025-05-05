package com.example.geradorgrade.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
// Import ViewBinding
// Import necessary UI components (Buttons, TextViews, etc.)
import com.example.geradorgrade.ui.viewmodel.MainViewModel

class UploadFragment : Fragment() {

    // private var _binding: FragmentUploadBinding? = null
    // private val binding get() = _binding!!
    private val viewModel: MainViewModel by activityViewModels() // Shared ViewModel

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // _binding = FragmentUploadBinding.inflate(inflater, container, false)
        // return binding.root
        println("UploadFragment created - Placeholder View") // Placeholder log
        return View(context) // Return a dummy view for now
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Setup UI listeners (e.g., button clicks for file selection)
        // binding.buttonSelectCatalog.setOnClickListener { selectFile("catalog") }
        // binding.buttonSelectHistory.setOnClickListener { selectFile("history") }
        // binding.buttonSelectCurriculum.setOnClickListener { selectFile("curriculum") }

        // Observe ViewModel LiveData (e.g., session ID, upload status, errors)
        // viewModel.sessionId.observe(viewLifecycleOwner) { sessionId -> ... }
        // viewModel.uploadStatusCatalog.observe(viewLifecycleOwner) { status -> updateUiForCatalog(status) }
        // viewModel.error.observe(viewLifecycleOwner) { error -> showError(error) }
    }

    // private fun selectFile(fileType: String) { ... }
    // private fun updateUiForCatalog(status: UploadStatus) { ... }
    // private fun showError(errorMessage: String?) { ... }

    override fun onDestroyView() {
        super.onDestroyView()
        // _binding = null // Clean up binding
    }
}

