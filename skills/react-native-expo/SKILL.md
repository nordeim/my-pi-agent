---
name: react-native-expo
description: "React Native (0.76+ with New Architecture: Fabric + TurboModules) + Expo (SDK 52+ with Expo Router v4) cross-platform mobile app workflow skill. Covers the New Architecture (Fabric renderer replacing the legacy bridge, TurboModules for synchronous native calls, React 18 concurrent features), Expo Application Services (EAS Build for cloud builds without local Xcode/Android Studio, EAS Submit for App Store + Play Store, EAS Update for OTA updates), Expo Router v4 (file-based routing like Next.js for native apps), the React mental model in native context (core components View/Text/Pressable/ScrollView/FlatList vs DOM elements, StyleSheet vs CSS, the 3 state managers: Zustand for app state, TanStack Query for server state, React Context for theme), navigation (Expo Router vs React Navigation 6 vs React Navigation 7 — when to choose), native module access via expo-* packages (camera, location, notifications, secure storage, haptics), testing (Jest + React Native Testing Library for unit/component, Maestro or Detox for E2E), and the deployment story (EAS Build + Submit for store apps, EAS Update for hotfixes). Use when building any iOS/Android/mobile web app with React Native + Expo — especially when the task involves New Architecture migration, Expo Router file conventions, EAS Build/Submit/Update setup, native module permissions, or OTA update strategy where idiomatic React Native differs from web React or from Flutter."
license: Proprietary. LICENSE.txt has complete terms
---

# React Native + Expo — Cross-Platform Mobile Workflow Skill

> **Target:** React Native 0.76+ (released November 2024, with **New Architecture enabled by default**: Fabric renderer + TurboModules + React 18 concurrent features) on **Expo SDK 52+** (released November 2024, with **Expo Router v4** for file-based routing). The Expo Application Services (EAS) — Build, Submit, Update — are the canonical cloud-native toolchain for building, deploying, and updating apps without local Xcode/Android Studio.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a React Native + Expo application. Trigger phrases include "React Native", "Expo", "Expo Router", "EAS Build", "EAS Submit", "EAS Update", "Fabric", "New Architecture", "TurboModule", "FabricRenderer", "Pressable", "FlatList", "StyleSheet", "Zustand", "TanStack Query", "React Navigation", "expo-camera", "expo-location", "expo-notifications", "expo-secure-store", "Maestro", "Detox", "app.config.ts", "expo prebuild", and any reference to an `app/` directory with `app/_layout.tsx` or `app.json` / `app.config.ts` config.

Do **not** use this skill for:
- **React Native ≤0.75** without New Architecture — the Fabric/TurboModules sections don't apply. Consider migrating.
- **Expo ≤SDK 50** without Expo Router — the routing sections assume Expo Router v4.
- **Bare React Native CLI** (without Expo) — different toolchain. The React Native concepts apply, but the Expo-specific sections (EAS, expo-* packages, app.config.ts) don't.
- **Flutter** — different language (Dart), different rendering model. See `flutter` skill.
- **Web-only React** — see React-related skills (`react19-ts6-vite8-tailwindv4-mvp`, etc.). React Native uses different primitives (no DOM).

## Quick Start

```bash
# Install Expo CLI (no global install needed — use npx)
# Create a new project with Expo Router v4 (file-based routing)
npx create-expo-app@latest myapp --template tabs
# OR the minimal template:
npx create-expo-app@latest myapp

cd myapp

# Install EAS CLI (Expo Application Services)
npm install -g eas-cli

# Log in to Expo (creates account at expo.dev if needed)
eas login

# Configure EAS for the project
eas build:configure

# Start dev server (Expo Go on your phone, or iOS/Android simulator)
npx expo start
# Press i = iOS simulator, a = Android emulator, s = web
# OR scan QR code with Expo Go app on your physical device
```

### Key commands

```bash
npx expo start                 # Start dev server (Metro bundler)
npx expo start --ios           # Start + open iOS simulator
npx expo start --android       # Start + open Android emulator
npx expo start --web           # Start + open web browser
npx expo start --clear         # Clear Metro cache (fixes weird bundling bugs)
npx expo start --tunnel        # Use ngrok tunnel (for testing across networks)

npx expo install <package>     # Install a package with version compatible with your Expo SDK
# (Use this instead of npm install for expo-* packages — ensures compatibility)

eas build --platform ios       # Cloud build for iOS (requires Apple Developer account)
eas build --platform android   # Cloud build for Android
eas build --profile preview    # Build using a custom profile from eas.json

eas submit --platform ios      # Submit to App Store Connect
eas submit --platform android  # Submit to Google Play Console

eas update --branch staging    # Push an OTA update to staging channel
eas update --branch production # Push an OTA update to production channel

eas build:configure            # Generate/refresh eas.json
eas credentials                # Manage Apple/Google credentials
```

---

## Project Structure (Expo Router v4 canonical layout)

Expo Router v4 uses **file-based routing** like Next.js — the directory structure under `app/` IS the navigation structure.

```
myapp/
├── app/                        # ← Expo Router: file-based routing lives here
│   ├── _layout.tsx             # Root layout (wraps every screen — auth provider, theme, etc.)
│   ├── index.tsx               # Home screen (/)
│   ├── (tabs)/                 # Route group — doesn't affect URL (parens = group)
│   │   ├── _layout.tsx         # Tab bar layout
│   │   ├── index.tsx           # First tab (/)
│   │   ├── search.tsx          # Second tab (/search)
│   │   └── profile.tsx         # Third tab (/profile)
│   ├── post/
│   │   ├── [id].tsx            # Dynamic route (/post/:id)
│   │   └── new.tsx             # Static route (/post/new)
│   ├── [...missing].tsx        # Catch-all route (404 handler)
│   └── +not-found.tsx          # 404 page
├── components/                 # Reusable components
│   ├── PostCard.tsx
│   └── UserAvatar.tsx
├── hooks/                      # Custom hooks
│   ├── useAuth.ts
│   └── usePosts.ts
├── stores/                     # Zustand stores (app state)
│   ├── authStore.ts
│   └── cartStore.ts
├── services/                   # API clients, external service wrappers
│   ├── api.ts
│   └── auth.ts
├── lib/                        # Utilities, constants
│   ├── utils.ts
│   └── constants.ts
├── assets/                     # Images, fonts, etc.
│   ├── images/
│   └── fonts/
├── app.config.ts               # Expo config (dynamic — can read env vars)
├── app.json                    # Expo config (static — usually you use one or the other)
├── package.json
├── tsconfig.json
├── eas.json                    # EAS Build/Submit/Update configuration
├── babel.config.js             # Babel config (usually minimal — Expo handles most)
├── metro.config.js             # Metro bundler config
└── .easignore                  # Files to exclude from EAS builds
```

### The `_layout.tsx` pattern

Layouts wrap all screens in their subtree. They're the place for providers (auth, theme, query client) and shared UI (header, tab bar).

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';
import { AuthProvider } from '@/hooks/useAuth';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { PaperProvider } from 'react-native-paper';

const queryClient = new QueryClient();

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <PaperProvider>
          <Stack>
            <Stack.Screen name="index" options={{ title: 'Home' }} />
            <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
            <Stack.Screen name="post/[id]" options={{ title: 'Post' }} />
          </Stack>
        </PaperProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

### Tab layout

```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Home, Search, User } from 'lucide-react-native';

export default function TabsLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#3B82F6' }}>
      <Tabs.Screen
        name="index"
        options={{ title: 'Home', tabBarIcon: ({ color }) => <Home color={color} /> }}
      />
      <Tabs.Screen
        name="search"
        options={{ title: 'Search', tabBarIcon: ({ color }) => <Search color={color} /> }}
      />
      <Tabs.Screen
        name="profile"
        options={{ title: 'Profile', tabBarIcon: ({ color }) => <User color={color} /> }}
      />
    </Tabs>
  );
}
```

---

## Core Mental Model: React in Native Context + Expo Managed Workflow + EAS Cloud Toolchain

React Native + Expo's distinctive paradigm is **React's component model driving native UI primitives, with a managed native layer via Expo's SDK and cloud build service.** Three things differentiate this stack from web React and from Flutter:

### 1. Core components map to native UI (no DOM)

```tsx
import { View, Text, Pressable, ScrollView, FlatList, Image, StyleSheet } from 'react-native';

// View = div, Text = p/span (text MUST be in <Text> — bare strings don't render)
// Pressable = button (with hover/pressed states)
// ScrollView = scrollable container (single child)
// FlatList = virtualized list (use for any list > 20 items — ScrollView renders all)
// Image = img (different API — source={require()} or source={{uri}})

function PostCard({ post, onPress }: { post: Post; onPress: () => void }) {
  return (
    <Pressable
      style={({ pressed }) => [styles.card, pressed && styles.cardPressed]}
      onPress={onPress}
    >
      <Image source={{ uri: post.imageUrl }} style={styles.image} />
      <View style={styles.content}>
        <Text style={styles.title}>{post.title}</Text>
        <Text style={styles.body} numberOfLines={2}>{post.body}</Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3, // Android shadow
  },
  cardPressed: { opacity: 0.7 },
  image: { width: '100%', height: 200, borderRadius: 8 },
  content: { marginTop: 12 },
  title: { fontSize: 18, fontWeight: '600', color: '#1F2937' },
  body: { fontSize: 14, color: '#6B7280', marginTop: 4 },
});
```

**Key differences from web React:**
- **`<div>` → `<View>`**, **`<p>`/`<span>` → `<Text>`** (bare strings don't render — must be inside `<Text>`)
- **No CSS files** — use `StyleSheet.create()` (validated at runtime, faster than inline objects)
- **No CSS cascade** — styles don't inherit (a `<Text>` doesn't inherit font from `<View>`)
- **`onClick` → `onPress`** — use `<Pressable>` (handles touch, hover, focus, disabled states)
- **`<img>` → `<Image>`** — different API (`source={{ uri: 'https://...' }}` or `source={require('./local.png')}`)
- **Flexbox defaults differ** — `flexDirection` defaults to `column` (web defaults to `row`)

### 2. The 3 state managers (each has a distinct role)

| Manager | Use for |
|---|---|
| **`useState` / `useReducer`** | Local component state (form fields, toggles, expand state) |
| **Zustand** | App-wide client state (auth user, theme, cart, offline cache) — simpler than Redux, no boilerplate |
| **TanStack Query** | Server state (API data, caching, mutations, optimistic updates) — the modern replacement for manual fetch + useState |
| **React Context** | Low-frequency app-wide config (theme, locale) — re-renders all consumers on change, don't use for high-frequency state |

```tsx
// stores/authStore.ts — Zustand
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  user: User | null;
  token: string | null;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setAuth: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'auth-storage', storage: createJSONStorage(() => AsyncStorage) }
  )
);

// Usage in a component — only re-renders when `user` changes
function Profile() {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  if (!user) return <LoginScreen />;
  return (
    <View>
      <Text>{user.name}</Text>
      <Pressable onPress={logout}><Text>Sign Out</Text></Pressable>
    </View>
  );
}
```

```tsx
// hooks/usePosts.ts — TanStack Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

export function usePosts() {
  return useQuery({
    queryKey: ['posts'],
    queryFn: () => api.get('/posts').then((r) => r.data),
  });
}

export function useCreatePost() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: CreatePostInput) => api.post('/posts', input),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['posts'] }),
  });
}

// Usage
function PostsScreen() {
  const { data: posts, isLoading, error, refetch } = usePosts();
  const createPost = useCreatePost();

  if (isLoading) return <ActivityIndicator />;
  if (error) return <ErrorView error={error} onRetry={refetch} />;

  return (
    <FlatList
      data={posts}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <PostCard post={item} />}
      onRefresh={refetch}
      refreshing={isLoading}
    />
  );
}
```

### 3. Expo Application Services (EAS) — cloud-native build pipeline

EAS is the killer feature of modern Expo. It replaces the painful local Xcode/Android Studio setup with cloud builds.

```jsonc
// eas.json
{
  "cli": { "version": ">= 5.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"   // Ad-hoc / internal testing
    },
    "production": {
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios": { "appleId": "you@example.com", "ascAppId": "1234567890", "appleTeamId": "ABCD123XYZ" },
      "android": { "serviceAccountKeyPath": "./google-service-account.json", "package": "com.example.myapp" }
    }
  }
}
```

```bash
# Cloud build (no local Xcode/Android Studio needed)
eas build --profile production --platform ios      # Takes ~10-20 min, builds on Expo's cloud
eas build --profile production --platform android

# Submit to stores
eas submit --platform ios --profile production      # Submits .ipa to App Store Connect
eas submit --platform android --profile production  # Submits .aab to Play Console

# OTA update (skip store review for JS-only changes)
eas update --branch production --message "Fix login bug"
```

**The OTA update story:** EAS Update lets you push JS-only changes (new screens, bug fixes, copy edits) directly to users without going through app store review. Native changes (new permissions, new native modules) still require a store release. This is the modern equivalent of "hot reloading in production."

---

## New Architecture (Fabric + TurboModules)

React Native 0.76+ ships with the New Architecture enabled by default. You don't need to do anything special to enable it, but you should understand what changed.

### What the New Architecture replaced

| Old (≤0.75) | New (0.76+) |
|---|---|
| **Legacy bridge** (async serial JSON messages between JS and native) | **Fabric** (sync, direct JSI calls — JavaScript Interface, no JSON serialization) |
| **Native modules** (async, bridge-bound) | **TurboModules** (sync or async, JSI-backed) |
| **Legacy renderer** (async layout, slow animations) | **Fabric renderer** (sync, concurrent, React 18 features work) |
| **Hermes JIT** (some platforms) | **Hermes with bytecode** (default on all platforms — faster startup) |

### What this means for you

Most app code doesn't change. But:

1. **React 18 concurrent features work properly now.** `useTransition`, `useDeferredValue`, `<Suspense>` — all functional.
2. **Animations are smoother.** `react-native-reanimated` 3+ uses JSI directly — no bridge overhead.
3. **Some old libraries don't work.** Libraries that haven't migrated to TurboModules need the **New Architecture interop layer** (enabled by default in 0.76+). If a library doesn't work, check its README for New Architecture support.
4. **JSI libraries work directly.** `react-native-sqlite-storage`, `react-native-mmkv`, `react-native-reanimated` — these use JSI and benefit from synchronous native calls.

### Checking if a library supports New Architecture

Search the library's README for "New Architecture" or "Fabric" or "TurboModule". The [React Native Directory](https://reactnative.directory/) shows compatibility status. Most popular libraries are migrated; obscure ones may not be.

---

## Navigation: Expo Router vs React Navigation

### Expo Router v4 (default for new Expo projects)

```tsx
// app/post/[id].tsx — file-based routing
import { useLocalSearchParams, Stack } from 'expo-router';

export default function PostScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return (
    <>
      <Stack.Screen options={{ title: `Post ${id}` }} />
      <PostDetail id={id} />
    </>
  );
}

// Navigation
import { router } from 'expo-router';
router.push('/post/123');       // Push onto stack
router.replace('/login');       // Replace (no back button)
router.back();                  // Pop
router.dismiss();               // Dismiss modal
```

### React Navigation 6/7 (the alternative — more flexible, more code)

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Post" component={PostScreen} options={({ route }) => ({ title: `Post ${route.params.id}` })} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigation
navigation.navigate('Post', { id: '123' });
navigation.goBack();
```

### When to choose which

| Project profile | Use |
|---|---|
| New Expo project | **Expo Router** (file-based, less boilerplate, deep links automatic) |
| Existing React Navigation codebase | Stay with React Navigation |
| Need complex nested navigation (e.g., tabs inside drawer inside stack) | React Navigation is more flexible |
| Web support (React Native for Web) | Expo Router (handles URL mapping automatically) |
| Want Next.js-style file conventions | Expo Router |

**Opinionated default:** Expo Router for new projects. The file-based routing is faster to set up, handles deep links automatically, and supports web targets.

---

## Native Module Access via `expo-*` packages

Expo provides a curated set of native modules (`expo-camera`, `expo-location`, `expo-notifications`, etc.) that work across iOS and Android with consistent APIs. Install with `npx expo install` (not `npm install`) — it picks a version compatible with your Expo SDK.

```bash
npx expo install expo-camera expo-location expo-notifications expo-secure-store expo-haptics expo-image-picker expo-file-system
```

### Common patterns

```tsx
// Camera
import { CameraView, useCameraPermissions } from 'expo-camera';

function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef<CameraView>(null);

  if (!permission) return <View />;
  if (!permission.granted) {
    return (
      <View>
        <Text>Camera permission required</Text>
        <Pressable onPress={requestPermission}><Text>Grant</Text></Pressable>
      </View>
    );
  }

  return (
    <CameraView ref={cameraRef} style={{ flex: 1 }} facing="back">
      <Pressable onPress={async () => {
        const photo = await cameraRef.current?.takePictureAsync();
        // Save photo, navigate, etc.
      }}>
        <Text>Take Photo</Text>
      </Pressable>
    </CameraView>
  );
}

// Location
import * as Location from 'expo-location';

async function getLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') throw new Error('Permission denied');

  const location = await Location.getCurrentPositionAsync({});
  return location.coords;
}

// Secure storage (Keychain on iOS, Keystore on Android)
import * as SecureStore from 'expo-secure-store';

await SecureStore.setItemAsync('auth_token', token);
const token = await SecureStore.getItemAsync('auth_token');
await SecureStore.deleteItemAsync('auth_token');

// Haptics
import * as Haptics from 'expo-haptics';
await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
```

### Permissions (iOS Info.plist + Android AndroidManifest.xml)

Some native modules require permission strings in `app.config.ts`:

```ts
// app.config.ts
export default {
  expo: {
    name: "MyApp",
    slug: "myapp",
    version: "1.0.0",
    ios: {
      infoPlist: {
        NSCameraUsageDescription: "We use the camera to take profile photos.",
        NSLocationWhenInUseUsageDescription: "We use location to show nearby posts.",
      },
    },
    android: {
      permissions: [
        "CAMERA",
        "ACCESS_COARSE_LOCATION",
        "ACCESS_FINE_LOCATION",
      ],
    },
    plugins: [
      [
        "expo-camera",
        { cameraPermission: "We use the camera to take profile photos." }
      ],
      [
        "expo-location",
        { locationAlwaysAndWhenInUsePermission: "We use location to show nearby posts." }
      ],
    ],
  },
};
```

---

## Configuration: `app.config.ts` (dynamic) vs `app.json` (static)

```ts
// app.config.ts — dynamic (can read env vars, run logic)
export default {
  expo: {
    name: process.env.NODE_ENV === 'production' ? 'MyApp' : 'MyApp (Dev)',
    slug: 'myapp',
    version: '1.0.0',
    orientation: 'portrait',
    userInterfaceStyle: 'automatic',
    splash: {
      image: './assets/splash.png',
      resizeMode: 'contain',
      backgroundColor: '#ffffff',
    },
    assetBundlePatterns: ['**/*'],
    ios: {
      supportsTablet: true,
      bundleIdentifier: 'com.example.myapp',
    },
    android: {
      adaptiveIcon: {
        foregroundImage: './assets/adaptive-icon.png',
        backgroundColor: '#ffffff',
      },
      package: 'com.example.myapp',
    },
    web: {
      favicon: './assets/favicon.png',
    },
    plugins: [
      'expo-router',
      ['./plugins/with-custom-config.ts', { apiKey: process.env.API_KEY }],
    ],
    extra: {
      eas: { projectId: 'your-eas-project-id' },
      apiUrl: process.env.EXPO_PUBLIC_API_URL,
    },
  },
};
```

**`app.config.ts` vs `app.json`:** use `app.config.ts` if you need env vars or conditional logic. Use `app.json` for static config (simpler, no eval overhead).

### Environment variables

```bash
# .env (NOT committed)
EXPO_PUBLIC_API_URL=https://api.example.com
EXPO_PUBLIC_STRIPE_KEY=pk_test_123
```

```tsx
// Anywhere in the app — prefix EXPO_PUBLIC_ is required for client access
const apiUrl = process.env.EXPO_PUBLIC_API_URL;
```

Variables prefixed with `EXPO_PUBLIC_` are inlined into the bundle at build time. Use EAS Build profiles to set per-environment values:

```jsonc
// eas.json
{
  "build": {
    "production": {
      "env": { "EXPO_PUBLIC_API_URL": "https://api.example.com" }
    },
    "staging": {
      "env": { "EXPO_PUBLIC_API_URL": "https://staging-api.example.com" }
    }
  }
}
```

---

## Testing

### Unit + component tests (Jest + React Native Testing Library)

```bash
npx expo install jest jest-expo @testing-library/react-native @testing-library/jest-native -- --save-dev
```

```tsx
// __tests__/PostCard.test.tsx
import { render, screen } from '@testing-library/react-native';
import PostCard from '@/components/PostCard';

const mockPost = {
  id: '1',
  title: 'Hello World',
  body: 'This is the body text that is long enough to need truncation.',
  imageUrl: 'https://example.com/image.png',
};

describe('PostCard', () => {
  it('renders title and truncated body', () => {
    render(<PostCard post={mockPost} onPress={jest.fn()} />);

    expect(screen.getByText('Hello World')).toBeTruthy();
    expect(screen.getByText(/This is the body text/)).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const onPress = jest.fn();
    render(<PostCard post={mockPost} onPress={onPress} />);

    screen.getByText('Hello World').parent?.props.onPress();
    expect(onPress).toHaveBeenCalledWith(mockPost.id);
  });
});
```

### E2E tests (Maestro — recommended for new projects)

Maestro is a YAML-based E2E testing framework that's simpler than Detox:

```yaml
# .maestro/flow.yaml
appId: ${MAESTRO_APP_ID}
---
- launchApp:
    clearState: true
- assertVisible: "Welcome"
- tapOn: "Sign In"
- assertVisible: "Email"
- tapOn:
    id: "email-input"
- inputText: "alice@example.com"
- tapOn:
    id: "password-input"
- inputText: "password123"
- tapOn: "Submit"
- assertVisible: "Hello, Alice"
```

```bash
# Install Maestro
curl -Ls "https://get.maestro.mobile.dev" | bash

# Run a flow
maestro test .maestro/flow.yaml
```

### Detox (alternative — more powerful, more setup)

Detox is the older E2E framework — more powerful but requires more setup. Use it if you need complex synchronization or grey-box testing.

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment: EAS Build + Submit + Update

### EAS Build (cloud builds)

```bash
# First-time setup
eas build:configure     # Generates eas.json

# Build for iOS (requires Apple Developer Program membership — $99/year)
eas build --profile production --platform ios
# EAS creates the .ipa on Expo's cloud, sends you a download link

# Build for Android
eas build --profile production --platform android
# EAS creates the .aab (App Bundle) for Play Store

# Build for both platforms
eas build --profile production --platform all
```

Builds take 10-30 minutes on Expo's free tier (faster on paid tiers). You get push notifications when complete.

### EAS Submit (store submission)

```bash
# Submit the latest iOS build to App Store Connect
eas submit --platform ios --latest

# Submit the latest Android build to Play Console
eas submit --platform android --latest
```

EAS handles credentials (Apple App Store Connect API key, Google service account) via `eas credentials`. First-time setup is interactive — EAS guides you through it.

### EAS Update (OTA updates for JS-only changes)

```bash
# Configure updates (one-time)
eas update:configure

# Push a JS-only update to production
eas update --branch production --message "Fix crash on profile screen"

# Push to staging for QA
eas update --branch staging --message "Test new login flow"
```

Users get the update on next app launch (within 30 seconds of opening). No app store review needed. The update channel (`branch`) maps to runtime versions — bump the runtime version in `app.config.ts` when you change native code (forces a store release).

```ts
// app.config.ts
export default {
  expo: {
    runtimeVersion: {
      policy: 'appVersion',    // Or 'fingerprint' for more granular control
    },
    updates: {
      url: 'https://u.expo.dev/your-project-id',
    },
  },
};
```

### Local builds (when you need Xcode/Android Studio)

For advanced scenarios (custom native code, debugging native issues), you can eject to bare React Native:

```bash
npx expo prebuild           # Generates ios/ and android/ directories
# Now you can open ios/MyApp.xcworkspace in Xcode, or android/ in Android Studio
# Build locally:
cd ios && pod install && xcodebuild ...
cd android && ./gradlew assembleRelease
```

**`prebuild` is reversible** — you can re-run `npx expo prebuild --clean` to regenerate native dirs from your `app.config.ts`. This is called the "CNG" (Continuous Native Generation) workflow — the source of truth is your config, not the native dirs.

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Using `ScrollView` for long lists.** `ScrollView` renders ALL children upfront — with 1000 items, you'll OOM the app. Use `FlatList` (virtualized — only renders visible items) for any list with >20 items. `FlashList` (from Shopify) is even faster — drop-in replacement for `FlatList`.

2. **Bare strings outside `<Text>`.** Web React renders bare strings fine. React Native doesn't — you'll get "Text strings must be rendered within a <Text> component" errors. Always wrap text in `<Text>`.

3. **Not using `Pressable` for interactive elements.** `TouchableOpacity` / `TouchableHighlight` are legacy. `Pressable` (introduced in RN 0.63) is the modern API — it handles press, hover, focus, disabled states with a single render-prop API. Use it for any tappable element.

4. **Inline styles instead of `StyleSheet.create`.** Inline `style={{...}}` creates a new object on every render — slow. `StyleSheet.create()` validates and caches styles at module load. The only time to use inline styles is for dynamic values that depend on props/state.

5. **Not memoizing expensive components.** React Native re-renders are expensive (native bridge calls). Wrap expensive components in `React.memo()` and pass stable callbacks (`useCallback`) and stable values (`useMemo`). But don't over-memoize — measure first.

6. **Forgetting to handle the keyboard.** Mobile keyboards cover content. Use `KeyboardAvoidingView` for forms, `Keyboard.dismiss()` on tap-outside, and `useKeyboardHeight` for custom layouts. Not handling this is the #1 form UX bug.

7. **Storing secrets in the JS bundle.** `EXPO_PUBLIC_*` variables are inlined at build time — anyone can extract them from the APK/IPA. Never put API secrets (Stripe secret keys, JWT signing keys) in the bundle. Use a backend proxy: the app calls your API, your API calls Stripe with the secret key.

8. **Not handling offline state.** Mobile networks are flaky. Use TanStack Query's `useQuery` with `staleTime` and `cacheTime` to serve cached data when offline. Show a clear "You're offline" indicator. Use `@react-native-community/netinfo` to detect connectivity changes.

9. **Ignoring platform-specific behavior.** iOS and Android have different conventions: back button (Android hardware back vs iOS swipe), status bar height, safe area insets, modal presentation styles. Use `Platform.OS` checks and `SafeAreaView` / `react-native-safe-area-context` for adaptive layouts.

10. **Skipping EAS Build in favor of local Xcode/Android Studio builds.** EAS Build runs on cloud — no local Xcode/Android Studio setup needed. The local setup is painful (Xcode is 12GB+, Android Studio is 8GB+, both require constant SDK updates). For 95% of projects, EAS Build is faster, simpler, and CI-friendly. Reserve local builds for advanced native debugging.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for React Native (project onboarding)
- `flutter` — Dart-based cross-platform mobile (different language, different rendering model, similar use case)
- `react19-ts6-vite8-tailwindv4-mvp` — Web React (similar component model, different primitives — no DOM in RN)
- `vue-3-nuxt` — Vue web framework (different framework, different ecosystem)
- `api-and-interface-design` — Type contract design (relevant for API client and TypeScript interfaces)
- `api-patterns` — REST API patterns (for the backend your RN app calls)
- `security-and-hardening` — OWASP-aware hardening (mobile-specific: certificate pinning, secure storage, jailbreak detection)
- `clean-code` — General coding standards applicable to TypeScript
- `testing-patterns` — Test pyramid, mocking strategies (RN-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for mobile projects

---

## Dependencies

Required (installed via `npx create-expo-app`):
- **Node.js** 20+
- **Expo SDK** 52+ (includes React Native 0.76+ with New Architecture)
- **React** 18.3+
- **React Native** 0.76+ (Fabric + TurboModules enabled by default)
- **Expo Router** v4 (file-based routing)
- **TypeScript** 5+ (default, can opt out but not recommended)
- **Metro** (bundler — bundled with Expo)
- **Hermes** (JavaScript engine — default in 0.70+)

### EAS CLI (install globally)

```bash
npm install -g eas-cli
```

### Common additions (install via `npx expo install`)

- `expo-router` — file-based routing (default in templates)
- `expo-secure-store` — encrypted key-value storage (Keychain / Keystore)
- `expo-camera` — camera access
- `expo-location` — GPS
- `expo-notifications` — push notifications
- `expo-haptics` — haptic feedback
- `expo-image-picker` — photo library access
- `expo-file-system` — file system access
- `expo-av` — audio/video playback and recording
- `expo-sqlite` — local SQLite database
- `@react-native-async-storage/async-storage` — unencrypted key-value storage
- `react-native-reanimated` — smooth animations (JSI-backed, New Architecture compatible)
- `react-native-gesture-handler` — gesture system
- `@tanstack/react-query` — server state management
- `zustand` — client state management
- `react-native-paper` — Material Design component library
- `@expo/vector-icons` — icon libraries (Feather, MaterialIcons, etc.)
- `lucide-react-native` — Lucide icon library
- `expo-font` — custom fonts
- `expo-splash-screen` — splash screen control
- `expo-status-bar` — status bar styling

### Testing

- `jest` + `jest-expo` + `@testing-library/react-native` — unit/component tests
- `@testing-library/jest-native` — additional Jest matchers
- `maestro` (install separately via `curl -Ls "https://get.maestro.mobile.dev" | bash`) — E2E testing
- `detox` — alternative E2E (more powerful, more setup)
