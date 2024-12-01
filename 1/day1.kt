import java.io.File
import kotlin.math.abs

fun getLists(): Pair<List<Int>, List<Int>> {
    val lines = File("./input.txt").readLines()
    
    val (l1, l2) = lines.map { line ->
        val (left, right) = line.split(Regex("\\s+"))
        left.toInt() to right.toInt()
    }.unzip()

    return l1.sorted() to l2.sorted()
}

fun part1(l1: List<Int>, l2: List<Int>): Int {
    return l1.zip(l2).sumOf { (a, b) -> abs(a - b) }
}

fun part2(l1: List<Int>, l2: List<Int>): Int {
    return l1.sumOf { lItem -> lItem * l2.count { it == lItem } }
}

fun main() {
    val (l1, l2) = getLists()
    part1(l1, l2).also(::println)
    part2(l1, l2).also(::println)
}