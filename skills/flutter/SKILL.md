---
name: flutter
description: "Flutter (Dart 3) cross-platform UI toolkit workflow skill — build iOS, Android, web, and desktop apps from a single codebase. Covers the widget-tree mental model (StatelessWidget vs StatefulWidget vs InheritedWidget), BuildContext and rebuilds, layout primitives (Row, Column, Stack, Container, Flex family, Expanded/Flexible), the state management decision tree (setState → InheritedWidget → Provider → Riverpod → Bloc → GetX), Navigation 2.0 router vs Navigation 1.0 (Navigator.push), pubspec.yaml and the pub.dev ecosystem, HTTP & JSON (http package + json_serializable codegen), forms and validation, implicit vs explicit animations, the testing pyramid (widget tests, integration tests, golden tests), platform channels for native code, and the per-platform deployment flows (iOS via Xcode + App Store Connect, Android via Gradle + Play Store, web, desktop). Use when building any mobile, desktop, or web app with Flutter — especially when the task involves state management choice, navigation patterns, or platform-specific deployment where idiomatic Flutter differs from web framework patterns."
license: Proprietary. LICENSE.txt has complete terms
---

# Flutter — Cross-Platform UI Toolkit Workflow Skill

> **Target:** Flutter 3.27+ (December 2024) on Dart 3.5+. Flutter compiles to native ARM code for iOS/Android, native desktop binaries for macOS/Windows/Linux, and HTML+Canvas+WebGL for web — all from a single Dart codebase. The widget-tree mental model is fundamentally different from React/Vue/Svelte's component model: there is no virtual DOM diffing, every state change rebuilds the affected widget subtree by default.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Flutter application. Trigger phrases include "Flutter", "Dart", "pubspec", "pub.dev", "widget", "StatelessWidget", "StatefulWidget", "BuildContext", "pub run", "flutter run", "flutter build", "MaterialApp", "Cupertino", "Riverpod", "Bloc", "Provider", "Getx", "Navigator.push", "MaterialPageRoute", "platform channel", and any reference to a `lib/main.dart` entry point or `pubspec.yaml` dependency file.

Do **not** use this skill for:
- **React Native** — different language (JS/TS), different rendering model (bridges to native UI). See React Native docs.
- **Native iOS (SwiftUI/UIKit)** — Apple-only, not cross-platform. Use Swift/SwiftUI directly.
- **Native Android (Jetpack Compose)** — Android-only. Use Kotlin/Compose directly.
- **Web-only projects** — Flutter web works but is heavier than React/Vue/Svelte for web-only targets. Use a web framework instead.
- **Flutter ≤3.0** — Impeller rendering engine, Dart 3 patterns, and Material 3 are 3.x+. Some patterns here require Flutter 3.10+.

## Quick Start

```bash
# Install Flutter SDK (multiple paths — pick one)
# 1. Official installer (recommended): https://docs.flutter.dev/get-started/install
# 2. Homebrew (macOS): brew install --cask flutter
# 3. FVM (Flutter Version Manager): brew tap leoafarias/fvm && brew install fvm && fvm install stable

flutter doctor                    # Verify install + toolchain (Xcode, Android SDK, etc.)

# Create a new project
flutter create my_app
cd my_app

flutter run                       # Run on the connected device/emulator (auto-selects)
flutter run -d chrome             # Run on Chrome (web)
flutter run -d ios                # Run on iOS simulator
flutter run -d android            # Run on Android emulator

flutter pub get                   # Install dependencies (like npm install)
flutter pub add <package>         # Add a dependency (updates pubspec.yaml)
flutter pub add dev:<package>     # Add a dev dependency
```

### Project structure (canonical layout)

```
my_app/
├── lib/                          # ← YOUR Dart code lives here
│   ├── main.dart                 # App entry point (void main() => runApp(MyApp()))
│   ├── app.dart                  # Root widget (MaterialApp or CupertinoApp)
│   ├── screens/                  # Full-screen widgets (home_screen.dart, settings_screen.dart)
│   ├── widgets/                  # Reusable widgets (custom_button.dart, post_card.dart)
│   ├── models/                   # Data models (user.dart, post.dart)
│   ├── services/                 # API clients, DB access, business logic
│   ├── providers/                # Riverpod/Provider state declarations
│   ├── repositories/             # Data layer abstraction (DB/API/cache)
│   └── utils/                    # Utilities (formatters, validators, constants)
├── test/                         # Unit + widget tests (mirrors lib/ structure)
├── integration_test/             # Integration tests (drive the whole app)
├── android/                      # Android-native project (Gradle, Kotlin/Java)
├── ios/                          # iOS-native project (Xcode, Swift/Objective-C)
├── web/                          # Web project (index.html, JS bootstrap)
├── macos/                        # macOS desktop project
├── windows/                      # Windows desktop project
├── linux/                        # Linux desktop project
├── assets/                       # Static assets (images, fonts, JSON, Lottie)
│   ├── images/
│   └── fonts/
├── pubspec.yaml                  # ← THE config file (deps, assets, Flutter config)
├── pubspec.lock                  # Locked dep versions (commit this)
├── analysis_options.yaml         # Dart analyzer config (lint rules)
└── .metadata                     # Flutter project metadata (managed by Flutter)
```

### Key commands

```bash
flutter run                       # Dev mode with hot reload
flutter run --release             # Release mode (optimized, no asserts)
flutter run --profile             # Profile mode (perf measurement, near-release)

# Hot keys during `flutter run`:
# r = hot reload (rebuilds widget tree, keeps state)
# R = hot restart (restarts app, loses state)
# q = quit

flutter build apk                # Android APK (debug/release)
flutter build appbundle          # Android App Bundle (Play Store)
flutter build ios                # iOS (requires Xcode)
flutter build web                # Web (outputs to build/web/)
flutter build macos              # macOS desktop
flutter build windows            # Windows desktop
flutter build linux              # Linux desktop

flutter test                     # Run all tests (test/ directory)
flutter test integration_test/   # Run integration tests
flutter analyze                  # Static analysis (Dart analyzer)
flutter format .                 # Format all Dart files (now `dart format .`)

flutter clean                    # Delete build/ and .dart_tool/ (fixes weird build errors)
flutter pub upgrade              # Upgrade deps within constraints
flutter pub upgrade --major-versions  # Upgrade to latest majors (may break)
```

---

## Core Mental Model: Widget Tree + Rebuilds

Flutter's distinctive paradigm is **everything is a widget, and widgets are immutable descriptions of configuration**. Three things differentiate Flutter from React/Vue/Svelte:

### 1. Everything is a widget

Layout, styling, padding, gestures, animations, navigation — all widgets. There are no separate "layout primitives" vs "components" vs "higher-order components" — it's widgets all the way down.

```dart
// A button with padding, a background color, and a tap handler
Padding(
  padding: EdgeInsets.all(16),
  child: Container(
    color: Colors.blue,
    child: GestureDetector(
      onTap: () => print('Tapped'),
      child: Center(
        child: Text(
          'Click me',
          style: TextStyle(color: Colors.white, fontSize: 16),
        ),
      ),
    ),
  ),
)
```

Every `Padding`, `Container`, `GestureDetector`, `Center`, `Text` is a widget. Nesting is deep — this is normal in Flutter. Don't fight it.

### 2. Widgets are immutable; StatefulWidgets hold mutable state via State objects

```dart
// StatelessWidget — no internal state, rebuilds when parent rebuilds
class Greeting extends StatelessWidget {
  const Greeting({super.key, required this.name});

  final String name;

  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name!');
  }
}

// StatefulWidget — has mutable state, can rebuild itself when state changes
class Counter extends StatefulWidget {
  const Counter({super.key});

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  void _increment() {
    setState(() {
      _count++;  // ← setState triggers a rebuild of this widget
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(onPressed: _increment, child: const Text('Increment')),
      ],
    );
  }
}
```

**Rule of thumb:** Start with `StatelessWidget`. Only switch to `StatefulWidget` when the widget needs to hold and mutate its own state. Most widgets are stateless — state should live in a state manager (Provider/Riverpod/Bloc) at a higher level, not in the widget.

### 3. setState rebuilds the widget subtree — not the whole app

When you call `setState(() { _count++; })`, Flutter marks this widget as dirty and rebuilds it on the next frame. The rebuild is **efficient** because:
- Flutter compares the new widget tree to the old one (element-by-element)
- If a widget is the same type with the same key, Flutter updates its configuration in place (no rebuild of its children unless their config changed)
- If a widget is a different type or different key, Flutter creates a new element

But `setState` still rebuilds the entire subtree under the StatefulWidget. For a counter button, that's fine. For a list of 1000 items, it's not — extract the items into separate widgets or use a state manager so only the relevant widget rebuilds.

### BuildContext — the widget's position in the tree

Every `build(BuildContext context)` method receives a `BuildContext`. It's the widget's address in the tree — used for:
- Looking up inherited state (`Theme.of(context)`, `Provider.of<T>(context)`)
- Navigator operations (`Navigator.push(context, ...)`)
- MediaQuery (`MediaQuery.of(context).size`)
- Showing dialogs (`showDialog(context: context, ...)`)

```dart
@override
Widget build(BuildContext context) {
  final theme = Theme.of(context);           // Look up app theme
  final size = MediaQuery.of(context).size;  // Screen size
  final isDark = theme.brightness == Brightness.dark;

  return Container(
    color: isDark ? Colors.black : Colors.white,
    width: size.width,
    child: Text('Hello', style: theme.textTheme.headlineMedium),
  );
}
```

**Important:** `context` is the position where the widget was inserted, NOT where it was built. If you save a `context` from `build()` and use it later (e.g., in an `onTap` callback), it might be stale. Use `Navigator.of(context)` patterns or `Builder` widgets to control which `context` is used.

---

## Layout: the Widget Catalog

Flutter's layout widgets fall into a few categories. Memorize these:

### Single-child layout widgets

| Widget | Use |
|---|---|
| `Container` | The Swiss-army knife: padding, margin, color, border, shadow, constraints. Use when you need multiple of these. |
| `Padding` | Just padding. Lighter than `Container` if you only need padding. |
| `Center` | Center a child within itself. |
| `Align` | Align a child to a specific corner/edge. |
| `SizedBox` | Force a specific width/height, or render an empty space. |
| `ConstrainedBox` | Apply min/max constraints to a child. |
| `AspectRatio` | Force a child to a specific aspect ratio. |
| `FractionallySizedBox` | Size a child as a fraction of parent. |
| `IntrinsicWidth` / `IntrinsicHeight` | Force a child to its content's intrinsic size (expensive — avoid). |
| `ClipRRect` / `ClipOval` | Clip a child to a rounded rect / oval. |
| `Transform` | Apply a matrix transform (rotate, scale, translate). |

### Multi-child layout widgets

| Widget | Use |
|---|---|
| `Column` | Vertical layout (children stack top-to-bottom). |
| `Row` | Horizontal layout (children stack left-to-right). |
| `Stack` | Children stack on top of each other (last child on top). |
| `ListView` | Scrollable vertical list. |
| `GridView` | Scrollable grid. |
| `Wrap` | Children flow like text (wrap to next line when full). |
| `Flow` | Custom flow with a delegate (advanced). |

### Flex children: `Expanded` vs `Flexible`

```dart
Row(
  children: [
    Expanded(            // Fills available space (force-fits)
      flex: 2,           // 2:1 ratio with the other Expanded
      child: Container(color: Colors.red),
    ),
    Expanded(
      flex: 1,
      child: Container(color: Colors.blue),
    ),
  ],
)

Row(
  children: [
    Flexible(            // Allows child to be smaller than available space
      fit: FlexFit.loose,
      child: Text('Hello'),  // Text is as wide as it needs to be, up to the available width
    ),
  ],
)
```

**Rule:** `Expanded` = `Flexible(fit: FlexFit.tight)` (child MUST fill the space). Use `Expanded` when you want a fixed-ratio split. Use `Flexible` when you want a max size but the child can be smaller.

### Constraints: the "tight vs loose" mental model

Flutter's layout protocol is **constraints down, sizes up**. A parent sends constraints (min/max width/height) to a child; the child picks a size within those constraints and reports it back up.

| Constraint type | Example | Behavior |
|---|---|---|
| **Tight** (min == max) | `SizedBox(width: 100)` | Child MUST be exactly 100px wide |
| **Loose** (min = 0, max = infinity) | `Center` | Child can be any size up to parent's max |
| **Bounded** (0 < min < max < infinity) | `Padding` | Child can be any size in range |
| **Unbounded** (max = infinity) | `ListView` inside `Column` | Child can be as big as it wants — DANGEROUS |

The #1 layout bug: putting a `ListView` (which wants unbounded height) inside a `Column` (which gives bounded height). Flutter throws "RenderBox was not laid out" or "Vertical viewport was given unbounded height". Fix: wrap the `ListView` in `Expanded`.

---

## State Management: the Decision Tree

Flutter has no built-in state manager (unlike React's Context or Vue's Pinia). You must choose one. The decision tree:

```
Is the state local to ONE widget?
├─ Yes → setState (StatefulWidget)
└─ No → Is the state shared across a FEW related widgets?
    ├─ Yes → InheritedWidget (or InheritedNotifier)
    └─ No → Is the state app-wide or complex?
        ├─ Simple app state → Provider (the official recommendation, simplest)
        ├─ Reactive/async/complex → Riverpod (modern, type-safe, testable)
        ├─ Event-driven, strict architecture → Bloc (Cubit for simpler cases)
        └─ "Just get it done" → GetX (opinionated, all-in-one — controversial)
```

### setState (local widget state)

```dart
class _CounterState extends State<Counter> {
  int _count = 0;

  void _increment() {
    setState(() { _count++; });
  }

  @override
  Widget build(BuildContext context) {
    return Text('$_count');
  }
}
```

Use for: form field focus, animation controller state, a toggle that doesn't affect anything else. **Do NOT** use for app-wide state — passing it down via constructor props becomes painful fast.

### Provider (official recommendation, simplest)

```yaml
# pubspec.yaml
dependencies:
  provider: ^6.1.0
```

```dart
// models/counter.dart
class Counter extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();  // ← Triggers rebuild of all listeners
  }
}

// main.dart
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => Counter(),
      child: const MyApp(),
    ),
  );
}

// Any widget
class CounterText extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final counter = context.watch<Counter>();   // Rebuilds when counter changes
    return Text('${counter.count}');

    // OR for one-shot read (no rebuild):
    // final counter = context.read<Counter>();
  }
}
```

### Riverpod (modern, type-safe, testable)

```yaml
# pubspec.yaml
dependencies:
  flutter_riverpod: ^2.5.0
```

```dart
// providers/counter_provider.dart
final counterProvider = StateNotifierProvider<Counter, int>((ref) {
  return Counter();
});

class Counter extends StateNotifier<int> {
  Counter() : super(0);
  void increment() => state++;
}

// Any widget
class CounterText extends ConsumerWidget {       // ← ConsumerWidget, not StatelessWidget
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);   // Rebuilds when count changes
    return Text('$count');
  }
}

// For one-shot read:
final count = ref.read(counterProvider);
```

Riverpod is the modern choice — better testability, no `BuildContext` dependency, compile-time safety. Prefer it for new projects.

### Bloc (event-driven, strict architecture)

```yaml
dependencies:
  flutter_bloc: ^8.1.0
```

```dart
// counter_bloc.dart
class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<Increment>((event, emit) => emit(state + 1));
    on<Decrement>((event, emit) => emit(state - 1));
  }
}

// Widget
class CounterText extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CounterBloc, int>(
      builder: (context, count) => Text('$count'),
    );
  }
}
```

Use Bloc when: the team wants strict separation of events/states/transitions, the app has complex async flows, or you want traceability for debugging (Bloc has time-travel debugging). Bloc has more boilerplate than Riverpod — use Cubit (Bloc's simpler sibling) if you don't need events.

### The recommendation for new projects

**Riverpod** is the modern default for new Flutter apps. It's type-safe, testable, and doesn't depend on `BuildContext`. Provider is fine for simple apps. Bloc is overkill unless you need strict event-driven architecture. GetX is popular but controversial — its global state mutability makes testing harder; avoid for serious projects.

---

## Navigation

Flutter has two navigation systems. Navigation 1.0 (imperative) is older but simpler. Navigation 2.0 (declarative) is the modern approach for complex apps with deep links.

### Navigation 1.0 (Navigator.push)

```dart
// Push a new screen
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const DetailScreen(),
  ),
);

// Pop back
Navigator.pop(context);

// Push and replace (no back button)
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (context) => const HomeScreen()),
);

// Push and clear the stack (e.g., after login)
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (context) => const HomeScreen()),
  (route) => false,  // Remove all previous routes
);

// Pass data
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => DetailScreen(postId: '123'),
  ),
);

// Receive data back
final result = await Navigator.push<String>(
  context,
  MaterialPageRoute(builder: (context) => const PickerScreen()),
);
if (result != null) {
  // Use the result
}
```

Navigation 1.0 is fine for most apps. Use it for: simple stacks, modals, bottom-tab navigation with a few screens.

### Navigation 2.0 (go_router — the modern declarative approach)

```yaml
dependencies:
  go_router: ^14.0.0
```

```dart
// main.dart
final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/posts/:id',
      builder: (context, state) => PostDetailScreen(
        id: state.pathParameters['id']!,
      ),
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(path: '/profile', builder: (context, state) => const ProfileScreen()),
        GoRoute(path: '/settings', builder: (context, state) => const SettingsScreen()),
      ],
    ),
  ],
  redirect: (context, state) {
    final isLoggedIn = /* check auth */;
    if (!isLoggedIn && state.path != '/login') {
      return '/login?redirect=${state.path}';
    }
    return null;
  },
);

void main() {
  runApp(MaterialApp.router(routerConfig: _router));
}

// Navigate
context.go('/posts/123');         // Replace current stack
context.push('/posts/123');       // Push onto stack
context.pop();                    // Pop back
```

Use `go_router` for: deep links, web URL support, complex nested navigation, auth-gated routes. It's the official recommendation for non-trivial apps.

---

## HTTP & JSON

### The `http` package (simple)

```yaml
dependencies:
  http: ^1.2.0
```

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<Post>> fetchPosts() async {
  final response = await http.get(Uri.parse('https://api.example.com/posts'));

  if (response.statusCode != 200) {
    throw Exception('Failed to load posts');
  }

  final List<dynamic> json = jsonDecode(response.body);
  return json.map((p) => Post.fromJson(p as Map<String, dynamic>)).toList();
}
```

### `json_serializable` (codegen — the canonical approach)

```yaml
dependencies:
  json_annotation: ^4.8.0
dev_dependencies:
  json_serializable: ^6.7.0
  build_runner: ^2.4.0
```

```dart
// models/post.dart
import 'package:json_annotation/json_annotation.dart';
part 'post.g.dart';

@JsonSerializable()
class Post {
  final String id;
  final String title;
  final String body;
  final DateTime? publishedAt;

  Post({required this.id, required this.title, required this.body, this.publishedAt});

  factory Post.fromJson(Map<String, dynamic> json) => _$PostFromJson(json);
  Map<String, dynamic> toJson() => _$PostToJson(this);
}
```

```bash
# Generate the .g.dart file
dart run build_runner build --delete-conflicting-outputs
# Watch mode for development
dart run build_runner watch --delete-conflicting-outputs
```

### Higher-level options

For larger apps, consider:
- **`dio`** — feature-rich HTTP client (interceptors, cancellation, FormData)
- **`retrofit`** — type-safe API client generator (annotations → codegen)
- **`chopper`** — similar to retrofit

---

## Forms & Validation

```dart
class LoginForm extends StatefulWidget {
  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _submit() {
    if (_formKey.currentState!.validate()) {
      // Form is valid — proceed
      final email = _emailController.text;
      final password = _passwordController.text;
      // ...
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
            validator: (value) {
              if (value == null || value.isEmpty) return 'Email is required';
              if (!value.contains('@')) return 'Enter a valid email';
              return null;
            },
          ),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'Password'),
            obscureText: true,
            validator: (value) {
              if (value == null || value.length < 8) {
                return 'Password must be at least 8 characters';
              }
              return null;
            },
          ),
          ElevatedButton(onPressed: _submit, child: const Text('Login')),
        ],
      ),
    );
  }
}
```

**Critical:** Always `dispose()` your `TextEditingController`s in `dispose()` to avoid memory leaks.

---

## Animations

### Implicit animations (animate a value change)

```dart
// AnimatedContainer — animates any change to its properties
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  color: _isExpanded ? Colors.blue : Colors.grey,
  width: _isExpanded ? 200 : 100,
  height: _isExpanded ? 200 : 100,
)

// Other implicit animation widgets:
// AnimatedOpacity, AnimatedPositioned, AnimatedAlign, AnimatedPadding,
// AnimatedDefaultTextStyle, AnimatedSwitcher, TweenAnimationBuilder
```

Use implicit animations when: you want to animate a value change with minimal code. Just change the value — the widget animates automatically.

### Explicit animations (full control via AnimationController)

```dart
class _MyWidgetState extends State<MyWidget> with TickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );
    _animation = CurvedAnimation(parent: _controller, curve: Curves.easeInOut);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();   // ← MANDATORY
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _animation,
      child: const FlutterLogo(size: 100),
    );
  }
}
```

Use explicit animations when: you need precise control over the animation timeline (reverse, pause, repeat), custom curves per segment, or choreographed multi-widget animations.

---

## Testing

Flutter has 3 test types in the testing pyramid:

### 1. Unit tests (test logic, no widgets)

```dart
// test/utils/validator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/utils/validator.dart';

void main() {
  group('Validator', () {
    test('returns null for valid email', () {
      expect(Validator.email('alice@example.com'), isNull);
    });

    test('returns error for invalid email', () {
      expect(Validator.email('not-an-email'), 'Enter a valid email');
    });
  });
}
```

### 2. Widget tests (test a widget in isolation)

```dart
// test/widgets/counter_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/widgets/counter.dart';

void main() {
  testWidgets('Counter increments when button tapped', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: Counter()));

    expect(find.text('0'), findsOneWidget);

    await tester.tap(find.byType(ElevatedButton));
    await tester.pump();   // Rebuild the widget

    expect(find.text('1'), findsOneWidget);
  });
}
```

### 3. Integration tests (test the whole app on a real device)

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('User can log in', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(const Key('email-field')), 'alice@example.com');
    await tester.enterText(find.byKey(const Key('password-field')), 'password');
    await tester.tap(find.byKey(const Key('login-button')));
    await tester.pumpAndSettle();

    expect(find.text('Welcome, Alice'), findsOneWidget);
  });
}
```

```bash
flutter test                          # Unit + widget tests
flutter test integration_test/       # Integration tests
flutter test --coverage              # With coverage
```

### Golden tests (visual regression)

```dart
testWidgets('Counter looks correct', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: Counter()));
  await expectLater(find.byType(Counter), matchesGoldenFile('counter.png'));
});
```

```bash
flutter test --update-goldens        # Update golden images
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Platform Channels (calling native code)

When you need to call platform-specific native code (iOS Swift/Objective-C, Android Kotlin/Java), use platform channels.

```dart
// Dart side
import 'package:flutter/services.dart';

class BatteryLevel {
  static const platform = MethodChannel('samples.flutter.dev/battery');

  static Future<int> getBatteryLevel() async {
    try {
      final int result = await platform.invokeMethod('getBatteryLevel');
      return result;
    } on PlatformException catch (e) {
      throw Exception('Failed to get battery level: ${e.message}');
    }
  }
}
```

```swift
// iOS — ios/Runner/AppDelegate.swift
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
  override func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: ...) -> Bool {
    let controller = window?.rootViewController as! FlutterViewController
    let batteryChannel = FlutterMethodChannel(
      name: "samples.flutter.dev/battery",
      binaryMessenger: controller.binaryMessenger
    )
    batteryChannel.setMethodCallHandler { call, result in
      if call.method == "getBatteryLevel" {
        UIDevice.current.isBatteryMonitoringEnabled = true
        let level = Int(UIDevice.current.batteryLevel * 100)
        result(level)
      } else {
        result(FlutterMethodNotImplemented)
      }
    }
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
```

```kotlin
// Android — android/app/src/main/kotlin/.../MainActivity.kt
class MainActivity : FlutterActivity() {
  private val CHANNEL = "samples.flutter.dev/battery"

  override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
    super.configureFlutterEngine(flutterEngine)
    MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
      if (call.method == "getBatteryLevel") {
        val level = getBatteryLevel()
        if (level != -1) result.success(level)
        else result.error("UNAVAILABLE", "Battery level not available.", null)
      } else result.notImplemented()
    }
  }

  private fun getBatteryLevel(): Int {
    val bm = getSystemService(BATTERY_SERVICE) as BatteryManager
    return bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
  }
}
```

For modern projects, consider using **FFI (Foreign Function Interface)** for synchronous C/Rust calls — it's faster than platform channels and works on all platforms including web.

---

## Deployment

### Android (Google Play Store)

```bash
# Build a release App Bundle (Play Store requirement)
flutter build appbundle --release

# Output: build/app/outputs/bundle/release/app-release.aab
```

1. Sign the bundle with a keystore (configure `android/key.properties` + `android/app/build.gradle`)
2. Upload to Play Console at https://play.google.com/console
3. Fill store listing, complete content rating, set pricing
4. Submit for review (1-3 days typical)

### iOS (App Store)

```bash
# Build the iOS app
flutter build ios --release --no-codesign

# Then open in Xcode to sign and archive
open ios/Runner.xcworkspace
# In Xcode: Product → Archive → Distribute App → App Store Connect
```

1. Configure signing (Apple Developer account, App ID, provisioning profile)
2. Set bundle ID, version, build number in Xcode
3. Archive and upload via Xcode or `altool` / Transporter
4. Submit for review in App Store Connect (24-48 hours typical)

### Web

```bash
flutter build web --release

# Output: build/web/
# Deploy to any static host (Firebase Hosting, Vercel, Netlify, GitHub Pages, S3)
```

### Desktop (macOS / Windows / Linux)

```bash
flutter build macos --release     # Output: build/macos/Build/Products/Release/
flutter build windows --release   # Output: build/windows/runner/Release/
flutter build linux --release     # Output: build/linux/x64/release/bundle/
```

Code-sign desktop builds for distribution. macOS requires Developer ID signing + notarization. Windows requires an EV code signing certificate. Linux can distribute unsigned via Flatpak/Snap/AppImage.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Deep widget trees.** A `build()` method that returns 15+ levels of nesting is hard to read and hard to test. Extract subtrees into separate `StatelessWidget`s. Flutter's widget composition is designed for this — don't fight it.

2. **Using `setState` for app-wide state.** `setState` rebuilds the widget AND all its children. For app-wide state (auth, theme, user data), use a state manager (Provider/Riverpod/Bloc) at the top of the tree so only the widgets that actually use the state rebuild.

3. **Blocking the UI thread.** Dart is single-threaded for UI work. Sync work that takes >16ms drops a frame. Use `compute()` for CPU-heavy work (runs in a separate isolate), `async`/`await` for I/O, and `Stream`/`Future` for everything else. Never call `sleep()` in a widget.

4. **Forgetting to `dispose()` controllers.** `TextEditingController`, `AnimationController`, `ScrollController`, `FocusNode` — all hold native resources. Always `dispose()` them in the `State`'s `dispose()` method. Memory leaks in Flutter are usually undisposed controllers.

5. **Using `FutureBuilder` without `initialData` or handling loading.** `FutureBuilder` rebuilds on every parent rebuild, which can re-trigger the future. Cache the future in `initState()` and handle `ConnectionState.waiting` explicitly.

6. **Hardcoding screen sizes.** `Container(width: 375)` assumes iPhone. Use `MediaQuery.of(context).size` or `LayoutBuilder` for responsive layouts. Test on small phones (320px) and large tablets (1024px+) — Flutter runs everywhere.

7. **Putting a `ListView` inside a `Column` without `Expanded`.** `ListView` wants unbounded height; `Column` gives bounded height. Flutter throws "Vertical viewport was given unbounded height". Wrap the `ListView` in `Expanded` (or use `CustomScrollView` with slivers).

8. **Using `BuildContext` across async gaps.** After `await`, the widget might have been disposed. `context.read<T>()` after `await` may throw. Capture the dependency before the `await`: `final nav = Navigator.of(context); await someAsync(); nav.push(...);`. Or check `if (!mounted) return;` after `await`.

9. **Not using `const` constructors.** `const Text('Hello')` is canonicalized — Flutter reuses the same instance, saving memory and rebuild time. Lint with `prefer_const_constructors`. Most widgets that take only constant args can be `const`.

10. **Treating Dart like JavaScript.** Dart has null safety (`String` vs `String?`), true generics (no type erasure), and an OO type system. Don't write `dynamic` everywhere. Don't use `var` for non-local variables. Enable strict analysis in `analysis_options.yaml` (`include: package:flutter_lints/flutter.yaml`) and treat warnings as errors.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Flutter (project onboarding)
- `api-and-interface-design` — Type contract design (relevant for Dart model classes and API clients)
- `api-patterns` — REST API patterns (for HTTP calls from Flutter)
- `security-and-hardening` — OWASP-aware hardening (mobile-specific concerns: certificate pinning, secure storage, jailbreak detection)
- `clean-code` — General coding standards applicable to Dart
- `testing-patterns` — Test pyramid, mocking strategies (Flutter-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Flutter projects

---

## Dependencies

Required (installed by `flutter create`):
- **Flutter SDK** 3.27+ (includes Dart 3.5+)
- **Dart** 3.5+ (bundled with Flutter)
- **Android Studio** or **VS Code** with Flutter plugin (recommended IDEs)
- **Android SDK** (for Android builds)
- **Xcode** 15+ (for iOS builds, macOS only)

Common additions (install via `flutter pub add`):
- **flutter_riverpod** (`flutter pub add flutter_riverpod`) — state management (modern recommendation)
- **provider** (`flutter pub add provider`) — state management (simpler, official)
- **flutter_bloc** (`flutter pub add flutter_bloc`) — state management (event-driven)
- **go_router** (`flutter pub add go_router`) — declarative navigation 2.0
- **http** (`flutter pub add http`) — simple HTTP client
- **dio** (`flutter pub add dio`) — feature-rich HTTP client
- **json_annotation** + **json_serializable** + **build_runner** — JSON codegen
- **freezed** (`flutter pub add freezed` + dev deps) — sealed classes / unions / copyWith codegen
- **shared_preferences** (`flutter pub add shared_preferences`) — simple key-value storage
- **sqflite** (`flutter pub add sqflite`) — SQLite database
- **hive** (`flutter pub add hive`) — fast NoSQL database
- **flutter_secure_storage** (`flutter pub add flutter_secure_storage`) — encrypted key-value (Keychain/Keystore)
- **path_provider** (`flutter pub add path_provider`) — file system paths
- **image_picker** (`flutter pub add image_picker`) — camera/gallery image picker
- **cached_network_image** (`flutter pub add cached_network_image`) — image caching
- **flutter_lints** (`flutter pub add dev:flutter_lints`) — recommended lint rules
- **integration_test** (bundled with Flutter) — integration test framework
- **mocktail** (`flutter pub add dev:mocktail`) — mocking library (preferred over mockito in Dart)
