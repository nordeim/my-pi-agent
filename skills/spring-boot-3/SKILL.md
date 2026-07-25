---
name: spring-boot-3
description: "Spring Boot 3.x (Java 21+ with virtual threads, released November 2023) enterprise backend workflow skill. Covers the IoC container (dependency injection via @Autowired / constructor injection, @Component / @Service / @Repository / @Controller stereotypes, @Configuration classes, @Bean methods), Spring Data JPA with Hibernate (repositories extending JpaRepository, @Entity models with @Table/@Column, JPQL vs native SQL, @Transactional boundaries, N+1 detection), Spring MVC @RestController with @GetMapping/@PostMapping/@PutMapping/@DeleteMapping, Spring Security 6 (SecurityFilterChain lambda DSL, method-level @PreAuthorize, OAuth2 Resource Server for JWT validation), Spring Boot Actuator for production observability (/health, /metrics, /info, /env), Spring Boot Starter dependencies (web, data-jpa, security, validation, actuator), application.yml profile-based config, Maven (pom.xml) vs Gradle (build.gradle) build tools, the Java 21 virtual threads story (spring.threads.virtual.enabled=true), JUnit 5 + Mockito + Spring Boot Test for testing, and the canonical deployment story (fat JAR via spring-boot-maven-plugin, Docker multi-stage build, JVM tuning). Use when building any Java enterprise web app, REST API, or microservice on Spring Boot 3 — especially when the task involves JPA entity design, repository methods, @Transactional boundaries, Spring Security filter chains, or Actuator endpoint configuration where idiomatic Spring differs from generic Java or from other web frameworks."
license: Proprietary. LICENSE.txt has complete terms
---

# Spring Boot 3 — Enterprise Java Backend Workflow Skill

> **Target:** Spring Boot 3.3+ (released May 2024) on Java 21+ (LTS, with virtual threads). Spring Boot 3.x requires Java 17 minimum and is built on the Jakarta EE 10 namespace (`jakarta.*` instead of `javax.*`). Spring Boot 3.2+ enables virtual threads via a single property (`spring.threads.virtual.enabled=true`), a game-changer for high-throughput request handling. Spring Framework 6.1+ is the underlying framework.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a Spring Boot 3 application. Trigger phrases include "Spring Boot", "Spring Framework", "Java", "Maven", "Gradle", "@RestController", "@Service", "@Repository", "@Autowired", "@Component", "@Bean", "@Configuration", "@Entity", "@Transactional", "JPA", "Hibernate", "Spring Data", "Spring Security", "Actuator", "application.yml", "application.properties", "pom.xml", "build.gradle", "@SpringBootApplication", and any reference to a `src/main/java/com/example/` package structure with `@SpringBootApplication`-annotated main class.

Do **not** use this skill for:
- **Spring Boot ≤2.x** — uses `javax.*` namespace, no virtual threads, different security DSL. Migrate to 3.x first.
- **Quarkus / Micronaut** — alternative Java frameworks with different conventions (build-time vs runtime IoC).
- **Plain Spring Framework (non-Boot)** — requires manual config; this skill assumes Boot's auto-configuration.
- **Android / Kotlin Multiplatform** — different ecosystems.
- **Other backend languages** (Go, Rust, Node.js, Python, Ruby) — see `go-web`, `rust-web`, `laravel-12`, `rails-8`, `django-6` skills.

## Quick Start

### Via Spring Initializr (the canonical scaffolder)

Visit https://start.spring.io/ (or use the IDE plugin — IntelliJ IDEA and VS Code both have integrations):

- **Project:** Maven (or Gradle — Gradle Kotlin DSL is the modern preference)
- **Language:** Java (or Kotlin — this skill is Java-first)
- **Spring Boot:** 3.3.x (or latest stable)
- **Group:** com.yourcompany
- **Artifact:** myapp
- **Packaging:** Jar
- **Java:** 21
- **Dependencies:** Spring Web, Spring Data JPA, PostgreSQL Driver, Spring Security, Validation, Spring Boot Actuator, Lombok (optional)

Click **Generate** → download ZIP → extract → import into IDE.

### Or via CLI

```bash
# Install Spring Boot CLI (optional)
brew install springboot

# Create a project
spring init \
  --dependencies=web,data-jpa,postgresql,security,validation,actuator \
  --java-version=21 \
  --group-id=com.example \
  --artifact-id=myapp \
  --package-name=com.example.myapp \
  myapp

cd myapp
./mvnw spring-boot:run      # Maven wrapper (or ./gradlew bootRun for Gradle)
# Dev server at http://localhost:8080
```

### Key commands (Maven)

```bash
./mvnw clean compile             # Compile
./mvnw test                      # Run tests
./mvnw test -Dtest=UserControllerTest  # Run one test class
./mvnw test -Dtest=UserControllerTest#shouldCreateUser  # Run one method
./mvnw package                   # Build JAR (runs tests first)
./mvnw package -DskipTests       # Build JAR without tests
./mvnw spring-boot:run           # Run in dev mode
./mvnw verify                    # Run all checks (tests + integration tests)
./mvnw clean install             # Build + install to local Maven repo
```

### Key commands (Gradle — modern preference)

```bash
./gradlew build                  # Build (runs tests)
./gradlew build -x test          # Build without tests
./gradlew test                   # Run tests
./gradlew test --tests "com.example.UserControllerTest"
./gradlew bootRun                # Run in dev mode
./gradlew bootJar                # Build fat JAR
./gradlew clean build            # Clean + build
```

---

## Project Structure (Spring Boot canonical layout)

Spring Boot enforces less structure than Rails/Laravel — Java packages are flexible. But there's a conventional layout:

```
myapp/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/myapp/         # ← Package matches group + artifact
│   │   │       ├── MyAppApplication.java  # ← Entry point (@SpringBootApplication)
│   │   │       ├── config/                # Configuration classes
│   │   │       │   ├── SecurityConfig.java
│   │   │       │   ├── OpenApiConfig.java
│   │   │       │   └── DatabaseConfig.java
│   │   │       ├── controller/            # @RestController classes
│   │   │       │   └── UserController.java
│   │   │       ├── service/               # @Service classes (business logic)
│   │   │       │   ├── UserService.java
│   │   │       │   └── EmailService.java
│   │   │       ├── repository/            # Spring Data JPA repositories (interfaces)
│   │   │       │   └── UserRepository.java
│   │   │       ├── model/                 # JPA @Entity classes + DTOs
│   │   │       │   ├── entity/            # Database entities
│   │   │       │   │   ├── User.java
│   │   │       │   │   └── Post.java
│   │   │       │   └── dto/               # Data Transfer Objects
│   │   │       │       ├── CreateUserRequest.java
│   │   │       │       └── UserResponse.java
│   │   │       ├── exception/             # Custom exceptions + global handler
│   │   │       │   ├── ResourceNotFoundException.java
│   │   │       │   └── GlobalExceptionHandler.java
│   │   │       └── security/              # Spring Security classes
│   │   │           ├── JwtTokenProvider.java
│   │   │           └── CustomUserDetailsService.java
│   │   └── resources/
│   │       ├── application.yml            # ← Main config
│   │       ├── application-dev.yml        # Dev profile overrides
│   │       ├── application-prod.yml       # Prod profile overrides
│   │       ├── db/migration/              # Flyway migrations (if using Flyway)
│   │       │   ├── V1__create_users.sql
│   │       │   └── V2__add_posts.sql
│   │       └── static/                    # Static assets (if serving UI)
│   └── test/
│       └── java/com/example/myapp/        # Tests mirror src/main structure
│           ├── controller/
│           │   └── UserControllerTest.java
│           ├── service/
│           │   └── UserServiceTest.java
│           └── MyAppApplicationTests.java # Context load test
├── pom.xml                                 # Maven config (or build.gradle for Gradle)
├── mvnw / mvnw.cmd                         # Maven wrapper (commit these)
├── .mvn/                                   # Maven wrapper config
├── Dockerfile
├── docker-compose.yml                      # For local Postgres etc.
└── README.md
```

### The entry point

```java
package com.example.myapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication                  // Combines @Configuration + @EnableAutoConfiguration + @ComponentScan
public class MyAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyAppApplication.class, args);
    }
}
```

`@SpringBootApplication` triggers:
1. **Auto-configuration** — Spring Boot inspects the classpath and configures beans based on what's present (e.g., if `spring-boot-starter-web` is on the classpath, an embedded Tomcat server is configured).
2. **Component scanning** — Spring scans the package of `MyAppApplication` and all sub-packages for `@Component` / `@Service` / `@Repository` / `@Controller` / `@Configuration` classes and registers them as beans.
3. **Configuration** — the class itself can define `@Bean` methods.

**Iron rule:** the package of `MyAppApplication` is the ROOT of component scanning. If you put it in `com.example.myapp`, only classes in `com.example.myapp.*` are scanned. Don't put it in `com.example` and then expect `com.othercompany` packages to be scanned.

---

## Core Mental Model: IoC Container + Convention-over-Configuration + Stereotypes

Spring's distinctive paradigm is **Inversion of Control via dependency injection, with the container managing object lifecycles.** Three things differentiate Spring Boot from other frameworks:

### 1. The IoC container manages everything (the application context)

```java
// You DON'T do this:
UserRepository repo = new UserRepository(dataSource);
UserService service = new UserService(repo);
UserController controller = new UserController(service);

// Spring does this FOR YOU. You just declare what you need:
@Service
public class UserService {
    private final UserRepository repo;

    // Constructor injection (preferred over @Autowired on fields)
    public UserService(UserRepository repo) {
        this.repo = repo;     // Spring injects the singleton UserRepository bean
    }
}

@RestController
public class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }
}
```

Spring's application context:
1. Scans for `@Component`-annotated classes (and its stereotypes: `@Service`, `@Repository`, `@Controller`, `@Configuration`)
2. Instantiates each as a singleton bean (by default)
3. Inspects constructor parameters and injects the matching beans
4. Manages the full lifecycle (initialization via `@PostConstruct`, destruction via `@PreDestroy`)

**Constructor injection is preferred** over `@Autowired` on fields because:
- It makes dependencies explicit (you can't instantiate the class without them)
- It enables immutability (fields can be `final`)
- It makes the class testable without Spring (just `new UserService(mockRepo)`)
- Spring ≥4.3 doesn't require `@Autowired` on constructors when there's only one

### 2. Stereotype annotations tell Spring what role a class plays

| Annotation | Use |
|---|---|
| `@Component` | Generic Spring-managed bean (the parent stereotype) |
| `@Service` | Business logic layer (semantically equivalent to `@Component` — for readability) |
| `@Repository` | Data access layer (enables automatic exception translation — converts SQLException → DataAccessException) |
| `@Controller` | Web controller returning a view (rare in modern REST APIs) |
| `@RestController` | `@Controller` + `@ResponseBody` — returns JSON/XML directly |
| `@Configuration` | Class containing `@Bean` methods (manual bean definitions) |
| `@Bean` | Method inside `@Configuration` that produces a bean |

```java
@Configuration
public class AppConfig {

    @Bean
    public ModelMapper modelMapper() {
        ModelMapper mapper = new ModelMapper();
        mapper.getConfiguration().setMatchingStrategy(MatchingStrategies.STRICT);
        return mapper;
    }

    @Bean
    public RestClient restClient() {
        return RestClient.builder()
            .baseUrl("https://api.example.com")
            .defaultHeader("Authorization", "Bearer " + apiKey)
            .build();
    }
}
```

Use `@Bean` for third-party classes you can't annotate (e.g., `ModelMapper`, `RestClient`). Use `@Component` stereotypes for your own classes.

### 3. Auto-configuration (the Spring Boot magic)

Spring Boot inspects your classpath and configures beans automatically:

| Starter on classpath | Auto-configuration |
|---|---|
| `spring-boot-starter-web` | Embedded Tomcat, `@RestController`, JSON serialization via Jackson |
| `spring-boot-starter-data-jpa` | Hibernate, `JpaRepository`, `LocalContainerEntityManagerFactoryBean` |
| `spring-boot-starter-security` | `SecurityFilterChain`, default form login + basic auth |
| `spring-boot-starter-actuator` | `/actuator/health`, `/actuator/metrics`, `/actuator/info` endpoints |
| `spring-boot-starter-validation` | Bean Validation (Hibernate Validator) auto-wired into `@Valid` |
| `spring-boot-starter-cache` | Cache abstraction (Redis, Caffeine, etc.) |
| `spring-boot-starter-oauth2-resource-server` | JWT validation for OAuth2-protected APIs |

You can override any auto-configuration by defining your own `@Bean` of the same type. Spring Boot's `@ConditionalOnMissingBean` annotation means your bean wins.

---

## Spring Data JPA: the ORM layer

Spring Data JPA is a wrapper around Hibernate that eliminates boilerplate DAO code. You define an interface, Spring generates the implementation.

### Entity classes

```java
package com.example.myapp.model.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.time.Instant;
import java.util.*;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @NotBlank
    @Email
    @Column(nullable = false, unique = true)
    private String email;

    @NotBlank
    @Column(nullable = false)
    private String name;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status = UserStatus.ACTIVE;

    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Post> posts = new ArrayList<>();

    @CreationTimestamp
    @Column(name = "created_at", updatable = false, nullable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    // No-args constructor (required by JPA)
    protected User() {}

    public User(String email, String name, String passwordHash) {
        this.email = email;
        this.name = name;
        this.passwordHash = passwordHash;
    }

    // Getters and setters (or use Lombok @Data / @Getter @Setter)
    public UUID getId() { return id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    // ... etc.
}
```

### Repositories (Spring generates the implementation)

```java
package com.example.myapp.repository;

import com.example.myapp.model.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID> {

    // Derived query — Spring parses the method name and generates the SQL
    Optional<User> findByEmail(String email);

    List<User> findByStatusOrderByCreatedAtDesc(UserStatus status);

    boolean existsByEmail(String email);

    // JPQL query (preferred for complex queries)
    @Query("SELECT u FROM User u WHERE u.status = :status AND u.createdAt > :since")
    List<User> findRecentActiveUsers(@Param("status") UserStatus status, @Param("since") Instant since);

    // Native SQL (use sparingly — JPQL is portable, native is not)
    @Query(value = "SELECT * FROM users WHERE email LIKE :pattern", nativeQuery = true)
    List<User> findByEmailPattern(@Param("pattern") String pattern);

    // Bulk update
    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.id IN :ids")
    int bulkUpdateStatus(@Param("ids") List<UUID> ids, @Param("status") UserStatus status);
}
```

### Using the repository

```java
@Service
public class UserService {
    private final UserRepository repo;

    public UserService(UserRepository repo) {
        this.repo = repo;
    }

    @Transactional
    public User createUser(CreateUserRequest request) {
        if (repo.existsByEmail(request.email())) {
            throw new EmailAlreadyExistsException(request.email());
        }
        User user = new User(request.email(), request.name(), hashPassword(request.password()));
        return repo.save(user);   // save() returns the persisted entity with generated ID
    }

    @Transactional(readOnly = true)
    public User getUser(UUID id) {
        return repo.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @Transactional(readOnly = true)
    public List<User> listActiveUsers() {
        return repo.findByStatusOrderByCreatedAtDesc(UserStatus.ACTIVE);
    }

    @Transactional
    public User updateUser(UUID id, UpdateUserRequest request) {
        User user = getUser(id);   // Loaded within the transaction — changes auto-flush
        if (request.name() != null) user.setName(request.name());
        if (request.email() != null) user.setEmail(request.email());
        return repo.save(user);    // save() does an UPDATE here (entity has an ID)
    }
}
```

### `@Transactional` boundaries (critical)

```java
@Service
public class UserService {
    // ...

    @Transactional                        // Read-write transaction (default)
    public User createUser(...) { /* ... */ }

    @Transactional(readOnly = true)       // Read-only — Spring can optimize
    public User getUser(UUID id) { /* ... */ }

    @Transactional
    public void transferMoney(UUID from, UUID to, BigDecimal amount) {
        Account src = repo.findById(from).orElseThrow();
        Account dst = repo.findById(to).orElseThrow();
        src.debit(amount);
        dst.credit(amount);
        // No repo.save() needed — Hibernate auto-flushes dirty entities at commit
    }
}
```

**Iron rules for `@Transactional`:**
1. Apply to **service** layer methods, not controller methods.
2. Default to `readOnly = true` for read operations (Hibernate skips dirty checking, faster).
3. Methods must be `public` (Spring uses proxies by default; private methods don't get proxied).
4. Self-invocation (`this.method2()` from `method1()`) does NOT trigger a new transaction — the proxy is bypassed. Move cross-transaction calls to a different bean.
5. Lazy loading only works inside a transaction. Accessing a lazy association outside a transaction throws `LazyInitializationException`.

### Avoiding N+1 queries

```java
// ❌ N+1: 1 query for users + N queries for posts (lazy-loaded per user)
List<User> users = repo.findAll();
users.forEach(u -> u.getPosts().size());   // Each access triggers a query

// ✅ Eager fetch via JPQL JOIN FETCH
@Query("SELECT DISTINCT u FROM User u LEFT JOIN FETCH u.posts WHERE u.status = :status")
List<User> findActiveWithPosts(@Param("status") UserStatus status);

// ✅ EntityGraph (declarative, no JPQL change)
@EntityGraph(attributePaths = "posts")
List<User> findByStatus(UserStatus status);

// ✅ Batch fetching (Hibernate config) — fetches lazy associations in batches
// spring.jpa.properties.hibernate.default_batch_fetch_size=50
```

---

## Spring MVC: @RestController

```java
package com.example.myapp.controller;

import com.example.myapp.model.dto.*;
import com.example.myapp.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    @GetMapping
    public List<UserResponse> listUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(required = false) UserStatus status
    ) {
        return service.listUsers(page, size, status);
    }

    @GetMapping("/{id}")
    public UserResponse getUser(@PathVariable UUID id) {
        return service.getUser(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        return service.createUser(request);
    }

    @PutMapping("/{id}")
    public UserResponse updateUser(@PathVariable UUID id, @Valid @RequestBody UpdateUserRequest request) {
        return service.updateUser(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable UUID id) {
        service.deleteUser(id);
    }

    // Custom response with headers
    @PostMapping("/{id}/avatar")
    public ResponseEntity<UploadResponse> uploadAvatar(
        @PathVariable UUID id,
        @RequestParam MultipartFile file
    ) {
        UploadResponse response = service.uploadAvatar(id, file);
        return ResponseEntity.created(URI.create("/api/users/" + id + "/avatar"))
            .eTag(response.version().toString())
            .body(response);
    }
}
```

### DTOs with Bean Validation

```java
package com.example.myapp.model.dto;

import jakarta.validation.constraints.*;

public record CreateUserRequest(
    @NotBlank @Email String email,
    @NotBlank @Size(min = 2, max = 100) String name,
    @NotBlank @Size(min = 8, max = 100) String password
) {}
```

The `@Valid` annotation on the controller method parameter triggers validation automatically. Failed validation returns a 400 response with field errors (handled by your `GlobalExceptionHandler`).

### Global exception handler

```java
package com.example.myapp.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.request.WebRequest;

import java.time.Instant;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex, WebRequest req) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(Instant.now(), 404, ex.getMessage(), req.getDescription(false)));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex, WebRequest req) {
        Map<String, String> fieldErrors = ex.getBindingResult().getFieldErrors().stream()
            .collect(java.util.stream.Collectors.toMap(f -> f.getField(), f -> f.getDefaultMessage()));
        return ResponseEntity.badRequest()
            .body(new ValidationErrorResponse(Instant.now(), 400, "Validation failed", req.getDescription(false), fieldErrors));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex, WebRequest req) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse(Instant.now(), 500, "Internal error", req.getDescription(false)));
    }

    public record ErrorResponse(Instant timestamp, int status, String message, String path) {}
    public record ValidationErrorResponse(Instant timestamp, int status, String message, String path, Map<String, String> errors) {}
}
```

---

## Spring Security 6

Spring Boot 3 ships with Spring Security 6, which uses the new lambda DSL (the old `.and()` chaining is removed).

```java
package com.example.myapp.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity   // Enables @PreAuthorize / @PostAuthorize on methods
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtFilter;

    public SecurityConfig(JwtAuthenticationFilter jwtFilter) {
        this.jwtFilter = jwtFilter;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())              // Disable CSRF for stateless APIs
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**", "/actuator/health", "/v3/api-docs/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}
```

### Method-level security

```java
@Service
public class PostService {

    @PreAuthorize("hasRole('ADMIN') or #post.author.id == authentication.principal.id")
    public Post updatePost(Post post, UpdatePostRequest request) { /* ... */ }

    @PreAuthorize("@postSecurity.canDelete(#id, authentication)")
    public void deletePost(UUID id) { /* ... */ }

    @PostAuthorize("returnObject.author.id == authentication.principal.id")
    public Post getOwnPost(UUID id) { /* ... */ }
}
```

### JWT authentication (OAuth2 Resource Server)

For modern APIs, use Spring Security's built-in OAuth2 Resource Server for JWT validation:

```yaml
# application.yml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth.example.com/realms/myapp
          # Spring fetches JWKS from issuer-uri + /.well-known/openid-configuration
```

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()));
        return http.build();
    }
}
```

The JWT is automatically validated against the issuer's JWKS, and `@AuthenticationPrincipal Jwt jwt` gives you access to claims in any controller.

---

## Configuration: application.yml + profiles

```yaml
# application.yml
spring:
  application:
    name: myapp

  datasource:
    url: ${DB_URL:jdbc:postgresql://localhost:5432/myapp}
    username: ${DB_USERNAME:postgres}
    password: ${DB_PASSWORD:postgres}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5

  jpa:
    hibernate:
      ddl-auto: validate          # Use Flyway for migrations; validate schema on boot
    properties:
      hibernate:
        default_batch_fetch_size: 50
        jdbc.batch_size: 50
        format_sql: false
    open-in-view: false            # Disable the anti-pattern OSIV (Open Session In View)

  threads:
    virtual:
      enabled: true                # Java 21 virtual threads — game-changer for throughput

  flyway:
    enabled: true
    locations: classpath:db/migration

server:
  port: 8080
  compression:
    enabled: true

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when-authorized
  metrics:
    tags:
      application: ${spring.application.name}

logging:
  level:
    com.example.myapp: DEBUG
    org.hibernate.SQL: WARN        # Don't log every SQL query in prod
```

### Profile-specific config

```yaml
# application-dev.yml
spring:
  jpa:
    properties:
      hibernate:
        format_sql: true
    show-sql: true
logging:
  level:
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
```

```yaml
# application-prod.yml
spring:
  jpa:
    show-sql: false
logging:
  level:
    root: WARN
    com.example.myapp: INFO
server:
  error:
    include-stacktrace: never      # Don't leak stack traces in prod
```

Activate with: `--spring.profiles.active=prod` or `SPRING_PROFILES_ACTIVE=prod` env var.

---

## Testing: JUnit 5 + Mockito + Spring Boot Test

### Unit tests (no Spring context)

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository repo;

    @InjectMocks
    private UserService service;

    @Test
    void shouldCreateUser() {
        when(repo.existsByEmail("alice@example.com")).thenReturn(false);
        when(repo.save(any(User.class))).thenAnswer(inv -> inv.getArgument(0));

        CreateUserRequest request = new CreateUserRequest("alice@example.com", "Alice", "password");
        User user = service.createUser(request);

        assertThat(user.getEmail()).isEqualTo("alice@example.com");
        verify(repo).save(any(User.class));
    }

    @Test
    void shouldThrowWhenEmailExists() {
        when(repo.existsByEmail("alice@example.com")).thenReturn(true);

        CreateUserRequest request = new CreateUserRequest("alice@example.com", "Alice", "password");
        assertThatThrownBy(() -> service.createUser(request))
            .isInstanceOf(EmailAlreadyExistsException.class);
    }
}
```

### Integration tests (full Spring context + DB)

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional                          // Rolls back after each test
class UserControllerIntegrationTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private UserRepository repo;

    @Test
    void shouldCreateUser() throws Exception {
        String body = """
            {"email": "alice@example.com", "name": "Alice", "password": "secret123"}
            """;

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(body))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.email").value("alice@example.com"))
            .andExpect(jsonPath("$.id").isNotEmpty());

        assertThat(repo.existsByEmail("alice@example.com")).isTrue();
    }
}
```

### Test slices (faster than @SpringBootTest)

```java
// Tests only the web layer (no service/repo)
@WebMvcTest(UserController.class)
class UserControllerWebTest {
    @Autowired private MockMvc mockMvc;
    @MockBean private UserService service;

    @Test
    void shouldReturnUserById() throws Exception {
        when(service.getUser(any(UUID.class)))
            .thenReturn(new UserResponse(UUID.randomUUID(), "alice@example.com", "Alice"));

        mockMvc.perform(get("/api/users/00000000-0000-0000-0000-000000000000"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Alice"));
    }
}

// Tests only the JPA layer (no web)
@DataJpaTest
class UserRepositoryTest {
    @Autowired private TestEntityManager em;
    @Autowired private UserRepository repo;

    @Test
    void shouldFindByEmail() {
        em.persistAndFlush(new User("alice@example.com", "Alice", "hash"));
        Optional<User> found = repo.findByEmail("alice@example.com");
        assertThat(found).isPresent();
    }
}
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment

### Fat JAR (the Spring Boot default)

```bash
./mvnw clean package -DskipTests
# Output: target/myapp-0.0.1-SNAPSHOT.jar
# This JAR contains ALL dependencies — run with:
java -jar target/myapp-0.0.1-SNAPSHOT.jar

# Or with profile + JVM tuning:
java -XX:MaxRAMPercentage=75 \
     -XX:+UseG1GC \
     -Dspring.profiles.active=prod \
     -jar myapp.jar
```

The fat JAR is self-contained — Tomcat is embedded, no servlet container installation required.

### Multi-stage Dockerfile

```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline                    # Cache deps
COPY src ./src
RUN mvn package -DskipTests

# Runtime stage — JRE only (smaller than JDK)
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=builder /app/target/myapp-*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", \
  "-XX:MaxRAMPercentage=75", \
  "-XX:+UseG1GC", \
  "-Dspring.profiles.active=prod", \
  "-jar", "app.jar"]
```

Final image size: ~250-400 MB (JRE + app). Smaller than Node/Python, larger than Go/Rust binaries.

### JVM tuning for containers

```bash
# Inside container (JDK 11+):
-XX:MaxRAMPercentage=75           # Use 75% of container memory (default is 25%)
-XX:+UseG1GC                      # Good default for most workloads
-XX:+ExitOnOutOfMemoryError       # Crash instead of zombie state — let the orchestrator restart
-XX:+AlwaysPreTouch               # Touch all memory pages at startup (avoids latency spikes)
-XX:MaxMetaspaceSize=256m         # Cap metaspace to prevent leaks
```

### Layered JAR (faster Docker rebuilds)

Spring Boot 3 supports layered JARs — each layer is a separate Docker layer, so dependencies (which change rarely) are cached separately from your code:

```dockerfile
FROM eclipse-temurin:21-jre-jammy AS extractor
WORKDIR /app
COPY target/myapp-*.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=extractor /app/dependencies/ ./
COPY --from=extractor /app/spring-boot-loader/ ./
COPY --from=extractor /app/snapshot-dependencies/ ./
COPY --from=extractor /app/application/ ./
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Field injection instead of constructor injection.** `@Autowired private UserService service;` on a field makes the class untestable without Spring and hides dependencies. Use constructor injection (no `@Autowired` needed since Spring 4.3 when there's one constructor). Make fields `final`.

2. **`Open Session in View` (OSIV).** Spring Boot enables `spring.jpa.open-in-view=true` by default — it keeps a Hibernate session open for the entire HTTP request. This masks lazy-loading issues (delays the `LazyInitializationException` to the controller layer) and adds hidden latency. **Always set `spring.jpa.open-in-view=false`** and define `@Transactional` boundaries explicitly on service methods.

3. **N+1 queries via lazy loading.** `user.getPosts()` inside a loop triggers a query per access. Use `JOIN FETCH` in JPQL or `@EntityGraph` to eager-load associations you'll need. The Hibernate Statistics log (`spring.jpa.properties.hibernate.generate_statistics=true`) reveals N+1 issues.

4. **Using `ddl-auto: update` in production.** Hibernate's auto-DDL can drop columns, rename them silently, or fail to detect type changes. Use `ddl-auto: validate` (verifies schema matches entities, doesn't modify) + a real migration tool (Flyway or Liquibase).

5. **Cross-cutting logic in controllers.** Controllers should be thin: parse request, call service, return response. Business logic goes in `@Service` classes. Validation goes in DTOs (`@Valid`). Error mapping goes in `@RestControllerAdvice`. Cross-cutting concerns (auth, logging) go in filters/interceptors.

6. **Not using `@Transactional(readOnly = true)` for reads.** Read-only transactions skip dirty checking (Hibernate doesn't track entity state changes), which is faster. Default to `readOnly = true` for query methods; only use read-write when you're modifying entities.

7. **Catching generic `Exception` in `@ExceptionHandler`.** A catch-all `@ExceptionHandler(Exception.class)` masks bugs — every unexpected error becomes a generic 500. Let unexpected exceptions propagate (Spring's default handler returns a 500 with proper logging). Catch specific exceptions you can handle meaningfully (404 for `ResourceNotFoundException`, 400 for `MethodArgumentNotValidException`, etc.).

8. **Using `@Autowired` on everything (including `@Configuration` beans).** `@Bean` methods in `@Configuration` classes are called by Spring — they don't need `@Autowired`. The class itself is `@Configuration` (which is a `@Component`), so Spring instantiates it. Only use `@Autowired` when you genuinely need field injection (which is rare).

9. **Not enabling virtual threads on Java 21+.** `spring.threads.virtual.enabled=true` is a one-line change that dramatically improves throughput for I/O-bound apps (database calls, external HTTP). Virtual threads cost ~1KB each (vs ~1MB for platform threads), so you can have millions of concurrent requests without thread-pool exhaustion. Spring Boot 3.2+ supports this.

10. **Using Lombok without understanding it.** Lombok (`@Data`, `@Builder`, `@Getter`, `@Setter`) reduces boilerplate but generates code at compile time. `@Data` on a JPA `@Entity` is dangerous — it generates `equals()` and `hashCode()` based on all fields, which can cause lazy-loading triggers and break entity equality before persistence. Use `@Getter @Setter` on entities, not `@Data`. For DTOs, `@Data` is fine.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for Spring Boot (project onboarding)
- `go-web` — Go web patterns (similar backend use case, no IoC container)
- `rust-web` — Rust web patterns (similar backend use case, ownership + traits vs IoC + annotations)
- `laravel-12` — PHP framework (similar enterprise feel, different language and conventions)
- `api-and-interface-design` — Type contract design (relevant for Java interfaces and DTOs)
- `api-patterns` — REST API patterns
- `security-and-hardening` — OWASP-aware hardening (Spring Security covers most OWASP concerns out of the box)
- `clean-code` — General coding standards applicable to Java
- `testing-patterns` — Test pyramid, mocking strategies (Spring-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for Java projects

---

## Dependencies

Required (managed via Maven or Gradle):
- **JDK** 21+ (Spring Boot 3 minimum is 17, but 21 LTS with virtual threads is recommended)
- **Maven** 3.9+ (or Gradle 8.x)
- **Spring Boot** 3.3+
- **Spring Framework** 6.1+

### Spring Boot Starters (add as needed via `pom.xml` or `build.gradle`)

| Starter | Use |
|---|---|
| `spring-boot-starter-web` | REST API with embedded Tomcat |
| `spring-boot-starter-data-jpa` | JPA + Hibernate + Spring Data repositories |
| `spring-boot-starter-data-redis` | Redis cache + session |
| `spring-boot-starter-data-mongodb` | MongoDB repositories |
| `spring-boot-starter-security` | Spring Security 6 |
| `spring-boot-starter-oauth2-resource-server` | JWT validation for OAuth2 APIs |
| `spring-boot-starter-oauth2-client` | OAuth2 / OIDC login (client side) |
| `spring-boot-starter-validation` | Bean Validation (Hibernate Validator) |
| `spring-boot-starter-actuator` | Production observability endpoints |
| `spring-boot-starter-cache` | Cache abstraction (`@Cacheable`, `@CacheEvict`) |
| `spring-boot-starter-async` | Async method execution (`@Async`) |
| `spring-boot-starter-quartz` | Quartz scheduler |
| `spring-boot-starter-batch` | Spring Batch for ETL jobs |
| `spring-boot-starter-webflux` | Reactive (non-blocking) alternative to MVC |
| `spring-boot-starter-graphql` | GraphQL API |
| `spring-boot-starter-amqp` | RabbitMQ |
| `spring-boot-starter-artemis` | ActiveMQ |

### Database drivers (add one)

| Driver | Use |
|---|---|
| `org.postgresql:postgresql` | PostgreSQL |
| `com.mysql:mysql-connector-j` | MySQL / MariaDB |
| `org.mariadb.jdbc:mariadb-java-client` | MariaDB (alternative) |
| `com.microsoft.sqlserver:mssql-jdbc` | SQL Server |
| `com.oracle.database.jdbc:ojdbc11` | Oracle |
| `org.xerial:sqlite-jdbc` | SQLite (dev/test only — not for production) |

### Common additions

- **Flyway** (`org.flywaydb:flyway-core`) — database migrations (preferred over Liquibase for SQL-first projects)
- **Liquibase** (`org.liquibase:liquibase-core`) — alternative migration tool (XML/YAML/JSON)
- **Lombok** (`org.projectlombok:lombok`) — boilerplate reduction (`@Data`, `@Builder`, `@Slf4j`) — use carefully on entities
- **MapStruct** (`org.mapstruct:mapstruct`) — type-safe DTO ↔ Entity mapping (compile-time codegen)
- **Springdoc OpenAPI** (`org.springdoc:springdoc-openapi-starter-webmvc-ui`) — Swagger UI + OpenAPI 3 docs at `/swagger-ui.html`
- **Resilience4j** (`io.github.resilience4j:resilience4j-spring-boot3`) — circuit breaker, retry, rate limiter (replaces Hystrix)
- **Micrometer + Prometheus** (`io.micrometer:micrometer-registry-prometheus`) — metrics export to Prometheus
- **Testcontainers** (`org.testcontainers:testcontainers`) — Docker-based integration tests (real Postgres, Redis, etc.)
- **spring-boot-devtools** (`org.springframework.boot:spring-boot-devtools`, dev only) — auto-restart on classpath change
