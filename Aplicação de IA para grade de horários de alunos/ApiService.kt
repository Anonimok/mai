package com.example.geradorgrade.network

import com.example.geradorgrade.model.PreferencesRequest
import com.example.geradorgrade.model.ScheduleOption
import com.example.geradorgrade.model.SessionResponse
import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit interface defining the API endpoints for communication with the Flask backend.
 */
interface ApiService {

    // --- Session --- //

    @POST("/api/session")
    suspend fun createSession(): Response<SessionResponse>

    // --- Uploads --- //

    @Multipart
    @POST("/api/upload/catalog")
    suspend fun uploadCatalog(
        @Header("X-Session-ID") sessionId: String,
        @Part file: MultipartBody.Part
    ): Response<ResponseBody> // Use ResponseBody for simple success/failure or a specific UploadResponse class

    @Multipart
    @POST("/api/upload/history")
    suspend fun uploadHistory(
        @Header("X-Session-ID") sessionId: String,
        @Part file: MultipartBody.Part
    ): Response<ResponseBody>

    @Multipart
    @POST("/api/upload/curriculum")
    suspend fun uploadCurriculum(
        @Header("X-Session-ID") sessionId: String,
        @Part file: MultipartBody.Part
    ): Response<ResponseBody>

    // --- Schedule --- //

    @POST("/api/schedule/preferences")
    suspend fun savePreferences(
        @Header("X-Session-ID") sessionId: String,
        @Body preferences: PreferencesRequest
    ): Response<ResponseBody> // Assuming simple success/failure response

    @POST("/api/schedule/generate")
    suspend fun generateSchedule(
        @Header("X-Session-ID") sessionId: String
    ): Response<List<ScheduleOption>> // Assuming the response is a list of schedule options

}

