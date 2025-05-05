package com.example.geradorgrade.model

import com.squareup.moshi.Json

/**
 * Data class representing a single schedule option returned by the backend.
 */
data class ScheduleOption(
    @Json(name = "courses") // Assuming the backend returns a list of courses under this key
    val courses: List<Course>,
    @Json(name = "total_credits") // Assuming the backend returns the total credits for this option
    val totalCredits: Int
)

