import java.io.File
import kotlin.math.abs

fun getReports(): List<List<Int>> {
    val lines: List<String> = File("/Users/olivia/projects/advent/src/2/input.txt").readLines()
    return lines.map { line -> line.trim().split(" ").map { it.toInt() } }
}

fun validateReport(rep: List<Int>): Boolean {    
    // Check if list is valid as-is
    if (isValidSequence(rep)) return true
    
    // Try removing each element
    for (i in rep.indices) {
        val newList = rep.toMutableList().apply { removeAt(i) }
        if (isValidSequence(newList)) return true
    }
    
    return false
}

// Helper function to check if a sequence is valid
private fun isValidSequence(rep: List<Int>): Boolean {
    if (rep.size < 2) return true
    
    // Determine direction from first valid difference
    var increasing: Boolean? = null
    for (i in 0 until rep.size - 1) {
        val diff = rep[i + 1] - rep[i]
        if (diff != 0) {
            increasing = diff > 0
            break
        }
    }
    if (increasing == null) return false // All numbers are the same
    
    // Check that all differences follow the direction and are <= 3
    for (i in 0 until rep.size - 1) {
        val diff = rep[i + 1] - rep[i]
        if (increasing && (diff <= 0 || diff > 3)) return false
        if (!increasing && (diff >= 0 || diff < -3)) return false
    }
    
    return true
}

fun day2() {
    val reps: List<List<Int>> = getReports()
    reps.count { validateReport(it) }.also(::println)
}
