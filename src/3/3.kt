import java.io.File

fun getInput(): String = File("${System.getProperty("user.dir")}/src/3/input.txt").readText()

sealed class Expr {
    object Do : Expr()
    object Dont : Expr()
    class Num(val n: Int) : Expr()
    class Mult(val a: Expr, val b: Expr) : Expr()
    class Seq(val e1: Expr, val e2: Expr) : Expr()
}

object Tokens {
    const val DO = """do\(\)"""
    const val DONT = """don't\(\)"""
    const val MUL = """mul\(([0-9]{1,3}),([0-9]{1,3})\)"""
}

fun parseInput(): Expr {
    val pattern = Regex("""${Tokens.MUL}|${Tokens.DO}|${Tokens.DONT}""")
    val matches = pattern.findAll(getInput())
    return matches.fold<MatchResult, Expr>(Expr.Num(0)) { acc, match ->
        when (match.value) {
            "do()" -> Expr.Seq(acc, Expr.Do)
            "don't()" -> Expr.Seq(acc, Expr.Dont)
            else -> {
                val (_, a, b) = match.groupValues
                Expr.Seq(acc, Expr.Mult(Expr.Num(a.toInt()), Expr.Num(b.toInt())))
            }
        }
    }
}

fun eval(e: Expr, doOp: Boolean): Pair<Int, Boolean> {
    return when (e) {
        is Expr.Num -> Pair(e.n, doOp)
        is Expr.Do -> Pair(0, true)
        is Expr.Dont -> Pair(0, false)
        is Expr.Mult -> {
            val (v1, doOp_) = eval(e.a, doOp)
            val (v2, doOp__) = eval(e.b, doOp_)
            Pair(if (doOp__) v1 * v2 else 0, doOp__)
        }
        is Expr.Seq -> { // sequence means addition in this language for some reason
            val (v1, doOp_) = eval(e.e1, doOp)
            val (v2, doOp__) = eval(e.e2, doOp_)
            Pair(v1 + v2, doOp__)
        }
    }
}

fun day3() {
    val expr = parseInput()
    val res = eval(expr, true)
    println(res.first)
}
