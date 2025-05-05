package com.example.geradorgrade.network

import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Singleton object to provide the Retrofit instance for API communication.
 */
object RetrofitClient {

    // Base URL of the Flask backend. For emulator, 10.0.2.2 points to host machine's localhost.
    // For physical device testing, replace with the host machine's network IP.
    private const val BASE_URL = "http://10.0.2.2:5000/"

    // Configure Moshi for Kotlin data class serialization/deserialization
    private val moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    // Configure OkHttpClient with logging (useful for debugging)
    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY // Log request and response bodies
    }

    private val okHttpClient = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .connectTimeout(30, TimeUnit.SECONDS) // Increase timeouts for potentially long operations
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
        .build()

    // Create the Retrofit instance
    private val retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .build()

    // Provide the ApiService implementation
    val apiService: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }
}

