package days
import java.io.File

fun getInput(): String {
    return File("/Users/olivia/projects/advent/src/3/input.txt").readText()
}

fun noIdidntBuiltAParser(input: String): Sequence<MatchResult> {
    val muls = """mul\(([0-9]+),([0-9]+)\)"""
    val dos = """do\(\)"""
    val donts = """don't\(\)"""
    val pattern = Regex("$muls|$dos|$donts")
    return pattern.findAll(input)
}

sealed class Expr {
    object Do : Expr()
    object Dont : Expr()
    class Mult(val a: Int, val b: Int) : Expr() {
        fun doOp(): Int = a * b
    }
}

fun day3() {
    val corrupted = getInput()
    val regexMatches = noIdidntBuiltAParser(corrupted)

    val operations = regexMatches
        .map {
            when (it.value) {
                "do()" -> Expr.Do
                "don't()" -> Expr.Dont
                else -> it.groupValues.let { (_, a, b) -> Expr.Mult(a.toInt(), b.toInt()) }
            }
        }
        .toList()

    val res = operations.fold(Pair(0, true)) { (acc, doOp), op ->
        when (op) {
            is Expr.Mult -> if (doOp) Pair(acc + op.doOp(), doOp) else Pair(acc, doOp)
            is Expr.Do -> Pair(acc, true)
            is Expr.Dont -> Pair(acc, false)
        }
    }

    println(res.first)
}
