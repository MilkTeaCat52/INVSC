# INVSC — INVariant Scala Compiler

> *"Your code is only as good as your invariants."*

The Scala compiler that judges your code like an Oxford tutor. INVSC checks that every loop in your Scala code has properly annotated invariants and variants, grades your code using the Oxford scoring system, and **refuses to compile** anything below α-β.

## 🎓 Grading System

| Grade | Meaning | Result |
|-------|---------|--------|
| **α** (Alpha) | First Class Honours | ✅ Compiles with fanfare |
| **αβ** (Alpha-Beta) | Upper Second | ✅ Compiles with mild approval |
| **β** (Beta) | Lower Second | ❌ Compilation DENIED |
| **γ** (Gamma) | Third Class | ❌ Compilation VIOLENTLY DENIED |

## 🚀 Installation

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Install INVSC
pip install -e .
```

You also need `scalac` on your PATH for actual compilation:
```bash
# macOS
brew install scala

# Or via Coursier (recommended)
cs install scala
```

## 📖 Usage

```bash
# Basic usage — check invariants and compile with scalac
invsc Main.scala

# Just check invariants, don't compile
invsc --no-compile Sort.scala

# Get raw JSON output
invsc --json Search.scala

# Force compile despite shameful grade (not recommended)
invsc --force Spaghetti.scala

# Skip the dramatic grade actions
invsc --no-action Main.scala

# Use a specific model
invsc --model gpt-4o-mini Main.scala
```

## 📝 What INVSC Checks

For every loop in your Scala code, INVSC verifies:

1. **Invariant annotation** — Does the loop have a comment specifying its invariant?
2. **Variant annotation** — Does the loop have a comment specifying its variant (termination measure)?
3. **Correctness** — Are the stated invariants actually correct?
4. **Variant decrease** — Does the variant actually decrease on each iteration?

## 🔊 Grade Actions

- **Alpha**: Triumphant announcement via macOS `say`
- **Alpha-Beta**: Mild acknowledgement
- **Beta**: Strongly worded letter to your Director of Studies
- **Gamma**: Threatens to delete your code (doesn't actually)

## 💡 Example

```scala
object Sum {
  def sum(arr: Array[Int]): Int = {
    var s = 0
    var i = 0
    // Invariant: s == sum of arr(0..i-1)
    // Variant: arr.length - i
    while (i < arr.length) {
      s += arr(i)
      i += 1
    }
    s
  }
}
```

## License

MIT — but your tutor's disappointment is forever.
