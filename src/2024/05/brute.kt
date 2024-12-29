import java.io.File

// Global rules map
private var rules: Map<Int, List<Int>> = mapOf()

data class ParseResult(
    val rules: Map<Int, List<Int>>,
    val pages: List<List<Int>>
)

fun parseInput(): ParseResult {
    val text = File("src/2024/05/input.txt").readText()
    val (rulesStr, pagesStr) = text.split("\n\n")
    
    val pages = pagesStr.lines()
        .map { line -> line.trim()j.split(",").map { it.toInt() } }

    // Parse rules
    val rulesMap = mutableMapOf<Int, MutableList<Int>>()
    rulesStr.lines().forEach { line ->
        val (before, after) = line.split("|")
        val afterNum = after.trim().toInt()
        val beforeNum = before.trim().toInt()
        rulesMap.getOrPut(afterNum) { mutableListOf() }.add(beforeNum)
    }

    return ParseResult(rulesMap, pages)
}

fun isValid(pages: List<Int>): Boolean {
    val posLookup = pages.withIndex().associate { (index, value) -> value to index }

    for ((afterNum, beforeNums) in rules) {
        val afterPos = posLookup[afterNum] ?: continue

        for (beforeNum in beforeNums) {
            posLookup[beforeNum]?.let { beforePos ->
                if (beforePos >= afterPos) return false
            }
        }
    }
    return true
}

data class PermutationResult(
    val isValid: Boolean,
    val permutation: List<Int>
)

fun checkPermutation(perm: List<Int>): PermutationResult {
    return PermutationResult(isValid(perm), perm)
}

fun <T> List<T>.permutations(): Sequence<List<T>> = sequence {
    if (isEmpty()) yield(emptyList())
    else {
        for (i in indices) {
            val element = get(i)
            val rest = toMutableList().apply { removeAt(i) }
            rest.permutations().forEach { subPerm ->
                yield(listOf(element) + subPerm)
            }
        }
    }
}

fun part1() {
    val parseResult = parseInput()
    rules = parseResult.rules
    val result = mutableListOf<List<Int>>()
    println("Processing examples")

    parseResult.pages.forEach { pages ->
        println("Processing permutation of size ${pages.size}")
        
        // Find first valid permutation
        val validPerm = pages.permutations()
            .asSequence()
            .map { checkPermutation(it) }
            .find { it.isValid }
            ?.permutation
        
        validPerm?.let { result.add(it) }
    }

    // Add middle numbers
    val total = result.sumOf { perm ->
        perm[perm.size / 2]
    }

    println(total)
}

fun day5() {
    part1()
}
