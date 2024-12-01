import java.io.File

fun getLists(): Pair<List<Int>, List<Int>> {
    val lines = File("./input.txt").readLines()
    
    val pairs = lines.map { line ->
        line.split("\\s+".toRegex())
            .map { it.trim().toInt() }
            .let { it[0] to it[1] }
    }

    val (l1, l2) = pairs.unzip()
    return l1.sorted() to l2.sorted()
}

fun main() {
    val (l1, l2) = getLists()
    val a1 = l1.zip(l2).sumOf { (a, b) -> kotlin.math.abs(a - b) }
    val a2 = l1.sumOf { lItem -> lItem * l2.count { it == lItem } }
    println(a1)
    println(a2)
}