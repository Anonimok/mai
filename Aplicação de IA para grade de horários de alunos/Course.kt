package com.example.geradorgrade.model

import com.squareup.moshi.Json

/**
 * Data class representing a single course within a schedule option.
 */
data class Course(
    @Json(name = "Código") // Match the JSON key from the backend
    val code: String,
    @Json(name = "Nome")
    val name: String,
    @Json(name = "Horários") // This is likely the formatted string like "Seg 08:20-10:10, Qua 08:20-10:10"
    val scheduleString: String,
    @Json(name = "Créditos")
    val credits: Int // Assuming credits are returned as Int
)

