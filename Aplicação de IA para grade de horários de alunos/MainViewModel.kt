package com.example.geradorgrade.ui.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.geradorgrade.network.RetrofitClient
import kotlinx.coroutines.launch
import java.io.IOException

class MainViewModel : ViewModel() {

    private val _sessionId = MutableLiveData<String?>()
    val sessionId: LiveData<String?> = _sessionId

    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading

    private val _error = MutableLiveData<String?>()
    val error: LiveData<String?> = _error

    init {
        // Automatically try to create a session when the ViewModel is created
        createSession()
    }

    fun createSession() {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            try {
                val response = RetrofitClient.apiService.createSession()
                if (response.isSuccessful && response.body() != null) {
                    _sessionId.value = response.body()!!.sessionId
                    println("Session created: ${_sessionId.value}") // Placeholder log
                } else {
                    _error.value = "Erro ao criar sessão: ${response.code()} ${response.message()}"
                    _sessionId.value = null
                }
            } catch (e: IOException) {
                _error.value = "Erro de rede ao criar sessão: ${e.message}"
                _sessionId.value = null
            } catch (e: Exception) {
                _error.value = "Erro inesperado ao criar sessão: ${e.message}"
                _sessionId.value = null
            }
            _isLoading.value = false
        }
    }

    // Function to clear error messages
    fun clearError() {
        _error.value = null
    }

    // Add other functions later for upload, preferences, schedule generation
}

