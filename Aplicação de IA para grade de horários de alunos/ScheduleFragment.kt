package com.example.geradorgrade.ui.fragment

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
// Import ViewBinding
// Import necessary UI components (Button, RecyclerView, ProgressBar, TextView)
// Import RecyclerView Adapter
import com.example.geradorgrade.ui.viewmodel.MainViewModel

class ScheduleFragment : Fragment() {

    // private var _binding: FragmentScheduleBinding? = null
    // private val binding get() = _binding!!
    private val viewModel: MainViewModel by activityViewModels() // Shared ViewModel
    // private lateinit var scheduleAdapter: ScheduleAdapter // RecyclerView Adapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // _binding = FragmentScheduleBinding.inflate(inflater, container, false)
        // return binding.root
        println("ScheduleFragment created - Placeholder View") // Placeholder log
        return View(context) // Return a dummy view for now
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Setup RecyclerView
        // setupRecyclerView()

        // Setup UI listeners
        // binding.buttonGenerateSchedule.setOnClickListener { viewModel.generateSchedule() }

        // Observe ViewModel LiveData
        // viewModel.sessionId.observe(viewLifecycleOwner) { sessionId -> updateGenerateButtonState() }
        // viewModel.preferencesSaved.observe(viewLifecycleOwner) { saved -> updateGenerateButtonState() } // Need a flag in ViewModel
        // viewModel.catalogUploaded.observe(viewLifecycleOwner) { uploaded -> updateGenerateButtonState() } // Need a flag in ViewModel
        // viewModel.isLoadingSchedule.observe(viewLifecycleOwner) { isLoading -> showLoading(isLoading) }
        // viewModel.scheduleOptions.observe(viewLifecycleOwner) { options -> displaySchedules(options) }
        // viewModel.error.observe(viewLifecycleOwner) { error -> showError(error) }

        // Initial state update for the button
        // updateGenerateButtonState()
    }

    // private fun setupRecyclerView() {
    //    scheduleAdapter = ScheduleAdapter()
    //    binding.recyclerViewSchedules.apply {
    //        adapter = scheduleAdapter
    //        layoutManager = LinearLayoutManager(context)
    //    }
    // }

    // private fun updateGenerateButtonState() {
    //    // Enable button only if session exists, catalog uploaded, and preferences saved
    //    val enabled = viewModel.sessionId.value != null && viewModel.catalogUploaded.value == true && viewModel.preferencesSaved.value == true
    //    binding.buttonGenerateSchedule.isEnabled = enabled
    // }

    // private fun showLoading(isLoading: Boolean) {
    //    binding.progressBar.visibility = if (isLoading) View.VISIBLE else View.GONE
    //    binding.recyclerViewSchedules.visibility = if (isLoading) View.GONE else View.VISIBLE
    // }

    // private fun displaySchedules(options: List<ScheduleOption>?) {
    //    if (options.isNullOrEmpty()) {
    //        binding.textViewStatus.text = "Nenhuma grade encontrada."
    //        binding.textViewStatus.visibility = View.VISIBLE
    //        scheduleAdapter.submitList(emptyList())
    //    } else {
    //        binding.textViewStatus.visibility = View.GONE
    //        scheduleAdapter.submitList(options)
    //    }
    // }

    // private fun showError(errorMessage: String?) {
    //    if (errorMessage != null) {
    //        binding.textViewStatus.text = errorMessage
    //        binding.textViewStatus.visibility = View.VISIBLE
    //        // Optionally use Snackbar as well
    //    }
    // }

    override fun onDestroyView() {
        super.onDestroyView()
        // _binding = null // Clean up binding
    }
}

