---
name: nestjs
description: "NestJS 10+ (TypeScript, Node.js 20+) enterprise backend workflow skill. Covers the Angular-inspired architecture (modules with @Module() decorators, controllers with @Controller() + @Get/@Post/@Put/@Delete route decorators, providers with @Injectable()), the IoC container (constructor injection, DI tokens, custom providers via useFactory/useClass/useValue, request-scoped vs singleton providers), DTOs with class-validator + class-transformer decorators (@IsEmail, @IsString, @IsOptional, ValidationPipe with whitelist/forbidNonWhitelisted/transform), exception filters (@Catch + @UseFilters) for centralized error handling, guards (@CanActivate) for authz, interceptors (NestInterceptor) for logging/caching/response transformation, pipes (ArgumentMetadata -> transformedValue) for validation/transformation, middleware (NestMiddleware), TypeORM + Prisma + Drizzle integration patterns, Passport-based auth (JwtStrategy, LocalStrategy), the testing utilities (Test.createTestingModule, Supertest, custom providers mock), Swagger/OpenAPI via @nestjs/swagger decorators, and Fastify adapter as a faster alternative to Express. Use when building any TypeScript enterprise backend, REST API, GraphQL API, or microservice on NestJS — especially when the task involves module organization, DI provider configuration, custom decorators, interceptor/guard/pipe composition, or testing with the testing module where idiomatic NestJS differs from Express/Fastify or from other IoC frameworks like Spring Boot."
license: Proprietary. LICENSE.txt has complete terms
---

# NestJS — Enterprise TypeScript Backend Workflow Skill

> **Target:** NestJS 10+ (released 2024) on Node.js 20+ with TypeScript 5+. NestJS is an Angular-inspired Node.js framework: modules, decorators, dependency injection, and a strict separation between controllers (HTTP layer), providers (business logic), and gateways (WebSocket). It supports both **Express** (default) and **Fastify** (faster, 2x throughput) as the underlying HTTP adapter. NestJS is the canonical choice for enterprise TypeScript backends — it brings the structure and DI patterns of Spring Boot / Angular to the Node.js ecosystem.

## When to Use This Skill

Use this skill whenever the user is building, debugging, or extending a NestJS application. Trigger phrases include "NestJS", "@Module", "@Controller", "@Injectable", "@Get", "@Post", "@UseGuards", "@UseInterceptors", "ValidationPipe", "JwtStrategy", "Passport", "Test.createTestingModule", "TypeORM", "@nestjs/swagger", "Fastify adapter", "nestjs/cli", and any reference to a `*.module.ts`, `*.controller.ts`, `*.service.ts`, or `*.dto.ts` file naming convention.

Do **not** use this skill for:
- **Express / Fastify / Hapi** (without NestJS) — these are lower-level; NestJS wraps them. Use general Node.js patterns instead.
- **Angular** — frontend framework, different domain. NestJS borrows Angular's DI patterns but is server-side only.
- **Spring Boot / .NET** — different languages, similar IoC concepts. See `spring-boot-3` and `dotnet-9` skills.
- **Fastify-only projects** — Fastify without NestJS is a different (lower-level) experience. This skill covers Fastify as a NestJS adapter.

Cross-reference: `framework-templates` has a NestJS section; this skill goes deep.

## Quick Start

```bash
# Install NestJS CLI globally
npm install -g @nestjs/cli

# Create a new project (interactive prompts for package manager)
nest new myapp
# Choose: npm, pnpm, yarn, or bun (pnpm is the modern recommendation)

cd myapp
pnpm install

# Dev server with hot reload
pnpm start:dev                  # http://localhost:3000

# Generate a resource (module + controller + service + DTOs + tests)
nest generate resource users
# Creates: src/users/users.module.ts, users.controller.ts, users.service.ts,
#          dto/create-user.dto.ts, dto/update-user.dto.ts, users.controller.spec.ts

# Other generators
nest g module posts
nest g controller posts
nest g service posts
nest g provider posts
nest g middleware logger
nest g guard auth
nest g interceptor logging
nest g pipe validation
nest g filter all-exceptions
nest g gateway events                # WebSocket gateway
```

### Key commands

```bash
pnpm start:dev                   # Dev mode with --watch (HMR-like reload)
pnpm start:debug                 # Dev mode with --inspect (Node debugger)
pnpm build                       # Production build to dist/
pnpm start:prod                  # Run the production build
pnpm test                        # Run Jest unit tests
pnpm test:watch                  # Watch mode
pnpm test:e2e                    # Run e2e tests (separate config)
pnpm test:cov                    # With coverage
pnpm lint                        # ESLint

# CLI shortcuts
nest g resource <name>           # Full CRUD scaffold
nest g module <name>
nest g controller <name>
nest g service <name>
nest g guard <name>
```

---

## Project Structure (NestJS canonical layout)

NestJS enforces a strict module-based structure. Each feature is a self-contained module with its own controller, service, DTOs, and tests.

```
myapp/
├── src/
│   ├── main.ts                  # Entry point: bootstrap NestFactory + global pipes/filters
│   ├── app.module.ts            # Root module — imports all feature modules
│   ├── app.controller.ts        # Root controller (usually just /health)
│   ├── app.service.ts
│   ├── common/                  # Cross-cutting concerns
│   │   ├── decorators/          # Custom decorators (@CurrentUser, @Roles)
│   │   ├── filters/             # Exception filters (HttpExceptionFilter)
│   │   ├── guards/              # Auth guards (JwtAuthGuard, RolesGuard)
│   │   ├── interceptors/        # LoggingInterceptor, TransformInterceptor
│   │   ├── pipes/               # Custom validation pipes
│   │   ├── middleware/          # LoggerMiddleware
│   │   └── dto/                 # Shared DTOs (PaginationDto, PaginationResultDto)
│   ├── config/                  # Config module (validated env vars via @nestjs/config)
│   │   ├── config.module.ts
│   │   ├── configuration.ts
│   │   └── validation.schema.ts # Joi/Zod schema for env validation
│   ├── database/                # Database module (TypeORM/Prisma/Drizzle)
│   │   ├── database.module.ts
│   │   └── entities/            # TypeORM entities (if using TypeORM)
│   ├── auth/                    # Auth feature module
│   │   ├── auth.module.ts
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── strategies/          # Passport strategies (jwt.strategy.ts, local.strategy.ts)
│   │   ├── guards/              # JwtAuthGuard, LocalAuthGuard
│   │   └── dto/                 # LoginDto, RegisterDto
│   ├── users/                   # Users feature module
│   │   ├── users.module.ts
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── dto/
│   │   │   ├── create-user.dto.ts
│   │   │   └── update-user.dto.ts
│   │   ├── entities/
│   │   │   └── user.entity.ts
│   │   └── users.controller.spec.ts
│   └── posts/                   # Another feature module
│       └── ...
├── test/                        # E2E tests (Supertest-based)
│   ├── app.e2e-spec.ts
│   └── jest-e2e.json
├── nest-cli.json                # NestJS CLI config (compiler options, swagger plugin)
├── tsconfig.json
├── tsconfig.build.json
├── package.json
└── Dockerfile
```

### The module/controller/service/provider contract

NestJS code is organized into **modules** that contain **controllers** (HTTP layer) and **providers** (services, repositories, factories). This separation is enforced by convention and the DI container.

```typescript
// src/users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';

@Module({
  imports: [TypeOrmModule.forFeature([User])],   // Register TypeORM repo for User entity
  controllers: [UsersController],
  providers: [UsersService],                       // Register UsersService for DI
  exports: [UsersService],                         // Make UsersService importable by other modules
})
export class UsersModule {}
```

```typescript
// src/users/users.controller.ts
import { Controller, Get, Post, Body, Param, Patch, Delete, UseGuards } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { Roles } from '../common/decorators/roles.decorator';
import { RolesGuard } from '../common/guards/roles.guard';

@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)              // Apply to all routes in this controller
export class UsersController {
  constructor(private readonly usersService: UsersService) {}   // ← Constructor injection

  @Post()
  @Roles('admin')                                  // Custom decorator for role-based authz
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(+id);
  }

  @Patch(':id')
  @Roles('admin')
  update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.usersService.update(+id, updateUserDto);
  }

  @Delete(':id')
  @Roles('admin')
  remove(@Param('id') id: string) {
    return this.usersService.remove(+id);
  }
}
```

```typescript
// src/users/users.service.ts
import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './entities/user.entity';
import { CreateUserDto } from './dto/create-user.dto';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly usersRepository: Repository<User>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User> {
    const existing = await this.usersRepository.findOne({
      where: { email: createUserDto.email },
    });
    if (existing) {
      throw new ConflictException('Email already registered');
    }

    const user = this.usersRepository.create(createUserDto);
    return this.usersRepository.save(user);
  }

  async findAll(): Promise<User[]> {
    return this.usersRepository.find();
  }

  async findOne(id: number): Promise<User> {
    const user = await this.usersRepository.findOne({ where: { id } });
    if (!user) {
      throw new NotFoundException(`User #${id} not found`);
    }
    return user;
  }

  async update(id: number, updateUserDto: UpdateUserDto): Promise<User> {
    const user = await this.findOne(id);             // Throws if not found
    Object.assign(user, updateUserDto);
    return this.usersRepository.save(user);
  }

  async remove(id: number): Promise<void> {
    const user = await this.findOne(id);
    await this.usersRepository.remove(user);
  }
}
```

---

## Core Mental Model: IoC + Decorators + Pipes/Guards/Interceptors/Filters

NestJS's distinctive paradigm is **Angular-style dependency injection with a composable request pipeline.** Four things differentiate NestJS from Express/Fastify:

### 1. The IoC container (DI is mandatory, not optional)

```typescript
// Constructor injection — NestJS auto-resolves typed providers
@Injectable()
export class UsersService {
  constructor(
    private readonly usersRepository: Repository<User>,    // TypeORM repo
    private readonly emailService: EmailService,           // Custom service
    private readonly configService: ConfigService,         // @nestjs/config
  ) {}
}

// Custom providers (when you need factory logic or non-class tokens)
@Module({
  providers: [
    // useClass — default, explicit
    { provide: 'IUsersService', useClass: UsersService },

    // useValue — for mocks or config constants
    { provide: 'APP_CONFIG', useValue: { apiUrl: 'https://api.example.com' } },

    // useFactory — for objects requiring async setup
    {
      provide: 'REDIS_CLIENT',
      useFactory: async (configService: ConfigService) => {
        const client = createClient({ url: configService.get('REDIS_URL') });
        await client.connect();
        return client;
      },
      inject: [ConfigService],                              // Inject deps into the factory
    },

    // useExisting — alias one provider to another
    { provide: 'ExtendedUsersService', useExisting: UsersService },
  ],
})
export class AppModule {}
```

**Provider scopes:**
- `DEFAULT` (singleton) — one instance for the whole app (most services)
- `REQUEST` — new instance per HTTP request (use sparingly — kills performance)
- `TRANSIENT` — new instance every time it's injected (rare)

```typescript
@Injectable({ scope: Scope.REQUEST })
export class TenancyService {
  // New instance per request — can hold request-scoped tenant ID
}
```

**Iron rule:** Avoid REQUEST-scoped providers unless absolutely necessary. They break the singleton optimization and add overhead to every request. Most request-scoped data should go through `request.user` (set by a guard) or a `ClsModule` (async context) instead.

### 2. Decorators drive the routing and metadata

```typescript
@Controller('users')                              // Base path /users
@UseGuards(JwtAuthGuard)                          // Apply guard to all routes
@UseInterceptors(LoggingInterceptor)              // Apply interceptor to all routes
export class UsersController {

  @Post(':id/avatar')                             // POST /users/:id/avatar
  @UseInterceptors(FileInterceptor('file'))       // Route-specific interceptor
  uploadAvatar(
    @Param('id') id: string,                      // URL param
    @UploadedFile() file: Express.Multer.File,    // Uploaded file
    @Body() metadata: AvatarMetadataDto,          // Request body
    @Query('resize') resize?: boolean,            // Query param (optional)
    @Headers('user-agent') userAgent: string,     // Request header
    @Req() req: Request,                          // Full request (rare — prefer specific decorators)
    @CurrentUser() user: User,                    // Custom param decorator
  ) {
    return this.usersService.uploadAvatar(+id, file, metadata, user);
  }
}
```

NestJS's decorators are not just metadata — they drive the framework's behavior. The `@Param()`, `@Body()`, `@Query()`, `@Headers()` decorators tell NestJS what to extract from the request and where to inject it.

### 3. The request pipeline: middleware → guards → interceptors (before) → pipes → controller → interceptors (after) → exception filters

```
Request
   ↓
Middleware (NestMiddleware)          — logging, CORS, body parsing
   ↓
Guards (CanActivate)                 — authn/authz — returns true/false
   ↓
Interceptors (before controller)     — logging, caching, transform request
   ↓
Pipes (ArgumentMetadata → value)     — validation, transformation
   ↓
Controller method                    — business logic via service
   ↓
Interceptors (after controller)      — transform response, error handling
   ↓
Exception filters (if exception)     — convert exceptions to HTTP responses
   ↓
Response
```

The order matters — guards run before pipes (so unauthenticated requests don't waste time validating), and exception filters catch anything thrown by the controller or pipes.

### 4. DTOs with class-validator + ValidationPipe

```typescript
// src/users/dto/create-user.dto.ts
import { IsEmail, IsString, MinLength, MaxLength, IsOptional, IsInt, Min, Max } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(2)
  @MaxLength(100)
  name: string;

  @IsString()
  @MinLength(8)
  @MaxLength(100)
  password: string;

  @IsOptional()
  @IsInt()
  @Min(13)
  @Max(120)
  age?: number;
}
```

```typescript
// src/main.ts — enable ValidationPipe globally
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,                // Strip unknown properties
      forbidNonWhitelisted: true,     // Throw 400 if unknown properties present
      transform: true,                // Transform payloads to DTO instances (e.g., string → number)
      transformOptions: { enableImplicitConversion: true },
    }),
  );

  await app.listen(3000);
}
bootstrap();
```

With this global pipe, every `@Body()` decorated with a class-validator-annotated DTO is automatically validated. Failed validation returns a 400 with detailed field errors — no validation code in the controller.

---

## Exception Filters

NestJS has built-in exception handling. `HttpException` (and subclasses like `NotFoundException`, `BadRequestException`, `ConflictException`) automatically produce the right HTTP response. Custom exception filters let you format errors consistently.

```typescript
// src/common/filters/all-exceptions.filter.ts
import { Catch, ExceptionFilter, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Request, Response } from 'express';

@Catch()                                          // Catch ALL exceptions
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';

    // Log unexpected errors (not HttpExceptions)
    if (!(exception instanceof HttpException)) {
      this.logger.error(`Unexpected error: ${exception}`, (exception as Error).stack);
    }

    response.status(status).json({
      statusCode: status,
      message: typeof message === 'string' ? message : (message as any).message,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}

// Register globally in main.ts
app.useGlobalFilters(new AllExceptionsFilter());
```

---

## Guards (authn/authz)

```typescript
// src/auth/guards/jwt-auth.guard.ts
import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private readonly jwtService: JwtService) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractToken(request);

    if (!token) {
      throw new UnauthorizedException('Missing token');
    }

    try {
      const payload = await this.jwtService.verifyAsync(token, {
        secret: process.env.JWT_SECRET,
      });
      request['user'] = payload;                   // Attach to request for downstream use
    } catch {
      throw new UnauthorizedException('Invalid token');
    }

    return true;
  }

  private extractToken(request: any): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
```

```typescript
// src/common/decorators/roles.decorator.ts
import { SetMetadata } from '@nestjs/common';
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// src/common/guards/roles.guard.ts
import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!requiredRoles) {
      return true;                                 // No @Roles() decorator — allow
    }

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user?.roles?.includes(role));
  }
}

// Usage in controller
@Post()
@Roles('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
create(@Body() dto: CreateUserDto) { /* ... */ }
```

---

## Interceptors

Interceptors wrap the controller method — they can transform the request before, the response after, or short-circuit entirely (caching).

```typescript
// src/common/interceptors/logging.interceptor.ts
import { CallHandler, ExecutionContext, Injectable, NestInterceptor } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const method = request.method;
    const url = request.url;
    const now = Date.now();

    return next
      .handle()                                    // ← Call the controller method
      .pipe(
        tap(() => console.log(`${method} ${url} - ${Date.now() - now}ms`)),
      );
  }
}

// Response transformation interceptor (e.g., wrap all responses in { data: ... })
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, { data: T }> {
  intercept(context: ExecutionContext, next: CallHandler<T>): Observable<{ data: T }> {
    return next.handle().pipe(map((data) => ({ data })));
  }
}

// Caching interceptor (short-circuits if cached)
@Injectable()
export class CacheInterceptor implements NestInterceptor {
  private readonly cache = new Map<string, any>();

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const key = request.url;

    if (this.cache.has(key)) {
      return of(this.cache.get(key));              // Short-circuit — don't call controller
    }

    return next.handle().pipe(
      tap((response) => this.cache.set(key, response)),
    );
  }
}
```

---

## Auth: Passport + JWT

```bash
pnpm add @nestjs/passport passport passport-jwt @nestjs/jwt
pnpm add -D @types/passport-jwt
```

```typescript
// src/auth/strategies/jwt.strategy.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { UsersService } from '../../users/users.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private readonly usersService: UsersService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET,
    });
  }

  async validate(payload: { sub: number; email: string }) {
    const user = await this.usersService.findOne(payload.sub);
    if (!user) {
      throw new UnauthorizedException();
    }
    return user;                                   // Becomes req.user
  }
}

// src/auth/auth.module.ts
@Module({
  imports: [
    UsersModule,
    PassportModule,
    JwtModule.register({
      secret: process.env.JWT_SECRET,
      signOptions: { expiresIn: '1h' },
    }),
  ],
  providers: [AuthService, JwtStrategy],
  controllers: [AuthController],
  exports: [AuthService],
})
export class AuthModule {}

// src/auth/auth.service.ts
@Injectable()
export class AuthService {
  constructor(
    private readonly usersService: UsersService,
    private readonly jwtService: JwtService,
  ) {}

  async validateUser(email: string, password: string): Promise<User> {
    const user = await this.usersService.findByEmail(email);
    if (user && await bcrypt.compare(password, user.passwordHash)) {
      return user;
    }
    throw new UnauthorizedException('Invalid credentials');
  }

  async login(user: User): Promise<{ access_token: string }> {
    const payload = { sub: user.id, email: user.email };
    return { access_token: await this.jwtService.signAsync(payload) };
  }
}
```

---

## Database: TypeORM, Prisma, or Drizzle

NestJS supports all major Node.js ORMs. The choice matters:

| ORM | Use when |
|---|---|
| **TypeORM** | Most popular NestJS ORM. Decorator-based entities (`@Entity()`, `@Column()`). Active Record or Data Mapper. Has NestJS first-party integration (`@nestjs/typeorm`). |
| **Prisma** | Type-safe by default. Schema-first (`schema.prisma`). Excellent DX. No decorators — generates a client. Use `nestjs-prisma` package or a custom module. |
| **Drizzle** | SQL-like API, lightweight, no runtime overhead. Type-safe via TypeScript inference. Newest of the three — fast-growing. |
| **MikroORM** | Identity-map based, less boilerplate than TypeORM. Good for complex domains. |

```typescript
// TypeORM entity
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column()
  name: string;

  @Column({ select: false })                       // Don't include in SELECT by default
  passwordHash: string;

  @CreateDateColumn()
  createdAt: Date;
}

// Module registration
@Module({
  imports: [
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        url: config.get('DATABASE_URL'),
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: config.get('NODE_ENV') !== 'production',  // DEV ONLY
      }),
    }),
    TypeOrmModule.forFeature([User]),
  ],
})
export class DatabaseModule {}
```

---

## Swagger / OpenAPI

NestJS has a first-party Swagger module that auto-generates OpenAPI 3 specs from your decorators. With the CLI plugin (`@nestjs/swagger`), DTOs auto-document.

```typescript
// src/main.ts
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const config = new DocumentBuilder()
    .setTitle('My API')
    .setDescription('API description')
    .setVersion('1.0')
    .addBearerAuth()
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('docs', app, document);      // Serves at /docs

  await app.listen(3000);
}
```

```jsonc
// nest-cli.json — enable the Swagger CLI plugin for auto-DTO documentation
{
  "collection": "@nestjs/schematics",
  "sourceRoot": "src",
  "compilerOptions": {
    "deleteOutDir": true,
    "plugins": [{
      "name": "@nestjs/swagger",
      "options": {
        "introspectComments": true,
        "classValidatorShim": true,
        "dtoKeyOfComment": true
      }
    }]
  }
}
```

With the plugin, DTOs like `CreateUserDto` automatically get `@ApiProperty()` decorators inferred from class-validator annotations + JSDoc comments. No manual Swagger decorators needed.

---

## Fastify Adapter (2x faster than Express)

```bash
pnpm add @nestjs/platform-fastify fastify
```

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create<NestFastifyApplication>(
    AppModule,
    new FastifyAdapter({ logger: true }),
  );
  await app.listen(3000, '0.0.0.0');
}
bootstrap();
```

Fastify is ~2x faster than Express in benchmarks and has better TypeScript support. Most NestJS features work identically with either adapter. The main differences:
- File uploads use `@fastify/multipart` instead of `multer`
- Some Express-specific middleware doesn't work (rare)
- The `request` object has a different shape (`FastifyRequest` vs `Request`)

For new projects, default to **Fastify** unless you need an Express-specific package.

---

## Testing (Jest + Supertest + Test.createTestingModule)

### Unit tests (with mocked providers)

```typescript
// src/users/users.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

describe('UsersController', () => {
  let controller: UsersController;
  let service: Partial<Record<keyof UsersService, jest.Mock>>;

  beforeEach(async () => {
    service = {
      create: jest.fn(),
      findAll: jest.fn(),
      findOne: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [{ provide: UsersService, useValue: service }],
    }).compile();

    controller = module.get<UsersController>(UsersController);
  });

  it('should create a user', async () => {
    const dto = { email: 'a@b.c', name: 'Alice', password: 'password' };
    service.create.mockResolvedValue({ id: 1, ...dto });

    expect(await controller.create(dto)).toEqual({ id: 1, ...dto });
    expect(service.create).toHaveBeenCalledWith(dto);
  });

  it('should throw NotFoundException when user missing', async () => {
    service.findOne.mockRejectedValue(new NotFoundException());
    await expect(controller.findOne('999')).rejects.toThrow(NotFoundException);
  });
});
```

### E2E tests (with real app + Supertest)

```typescript
// test/app.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('UsersController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/users (POST)', async () => {
    const response = await request(app.getHttpServer())
      .post('/users')
      .send({ email: 'alice@example.com', name: 'Alice', password: 'password123' })
      .expect(201);

    expect(response.body).toHaveProperty('id');
    expect(response.body.email).toBe('alice@example.com');
  });

  it('/users (POST) - invalid email returns 400', async () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ email: 'not-an-email', name: 'Alice', password: 'password123' })
      .expect(400);
  });
});
```

Cross-reference: `testing-patterns` for general test pyramid / mocking strategies.

---

## Deployment

```bash
pnpm build                       # Outputs to dist/ (compiled JS)
node dist/main.js                # Run the production build
```

### Docker multi-stage build

```dockerfile
# Build stage
FROM node:20-slim AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# Runtime stage
FROM node:20-slim
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile --prod
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### PM2 (process manager)

```bash
pnpm add -g pm2
pm2 start dist/main.js --name myapp -i max    # Cluster mode (max = CPU cores)
pm2 logs myapp
pm2 status
pm2 restart myapp
pm2 save                                       # Save process list for auto-restart on reboot
pm2 startup                                    # Generate system startup script
```

---

## Top 10 Anti-Patterns (the most valuable section)

1. **Fat controllers with business logic.** Controllers should be 5-15 lines: parse request, call service, return response. Business logic goes in `@Injectable()` services. If your controller has `if`/`for`/`try-catch`, it's too fat.

2. **Using `synchronize: true` in production.** TypeORM's `synchronize: true` auto-creates schema from entities — convenient in dev, dangerous in prod (can drop columns silently on type changes). Use migrations: `pnpm typeorm migration:generate` + `pnpm typeorm migration:run`.

3. **REQUEST-scoped providers for request data.** REQUEST scope kills performance (new instance per request, can't be singleton-cached). Use `request.user` (set by a guard) or `nestjs-cls` (continuation-local storage) for request-scoped data instead.

4. **Not enabling `ValidationPipe` globally.** Without `app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))`, DTOs are just TypeScript interfaces — zero runtime validation. Always enable the global pipe with `whitelist` + `forbidNonWhitelisted` + `transform`.

5. **Cross-module imports without `exports`.** If `UsersModule` doesn't `exports: [UsersService]`, no other module can import it. The DI container throws "Nest can't resolve dependencies of the PostsService (?, +)". Always export the services you want other modules to use.

6. **Circular module dependencies.** `UsersModule` imports `PostsModule`, `PostsModule` imports `UsersModule` — circular. Fix: extract the shared logic into a third module both import, or use `forwardRef(() => OtherModule)` (last resort — usually indicates a design issue).

7. **Catching exceptions in controllers.** Let exceptions propagate to NestJS's exception layer. `throw new NotFoundException()` from the service → NestJS converts to a 404 automatically. Wrapping in try-catch and returning custom responses breaks the global exception filter.

8. **Not using `@nestjs/config` for env vars.** Direct `process.env.DATABASE_URL` is untyped, unvalidated, and can't be mocked in tests. Use `@nestjs/config` with a Joi/Zod validation schema — fail fast on boot if env is missing or malformed.

9. **Using Express by default without considering Fastify.** Fastify is ~2x faster and has better TypeScript support. The only reason to choose Express is if you depend on an Express-specific package. For new projects, default to Fastify.

10. **Not using the Swagger CLI plugin.** Without the `@nestjs/swagger` plugin in `nest-cli.json`, you have to manually add `@ApiProperty()` to every DTO field. With the plugin, DTOs auto-document from class-validator annotations + JSDoc. Set it up once in `nest-cli.json` and never write a manual `@ApiProperty` again.

---

## Cross-references

- `framework-templates` — CLAUDE.md generation template for NestJS (project onboarding)
- `spring-boot-3` — Java enterprise backend (similar IoC model — DI, stereotypes, interceptors ↔ filters)
- `dotnet-9` — .NET enterprise backend (similar IoC model — minimal APIs ↔ controllers, DI lifetimes)
- `go-web` — Go web patterns (contrast: no IoC, stdlib-first, errors-as-values)
- `fastapi-sqlalchemy` — Python async API (contrast: type-driven validation via Pydantic, async-first)
- `api-and-interface-design` — Type contract design (relevant for NestJS DTOs and interfaces)
- `api-patterns` — REST API patterns
- `security-and-hardening` — OWASP-aware hardening
- `clean-code` — General coding standards applicable to TypeScript
- `testing-patterns` — Test pyramid, mocking strategies (NestJS-specific syntax above; general principles there)
- `code-review-checklist` — 12-category code review checklist
- `git-workflow-and-versioning` — Branching/commit conventions for NestJS projects

---

## Dependencies

Required (installed via `nest new`):
- **Node.js** 20+ (or Bun 1.1+)
- **NestJS** 10+
- **TypeScript** 5+
- **Reflect-metadata** (required for decorators)
- **RxJS** 7+ (NestJS uses Observables extensively)
- **Express** (default adapter) OR **Fastify** (faster alternative)

### Common additions (install via `pnpm add`)

- `@nestjs/platform-fastify` + `fastify` — Fastify adapter (2x faster than Express)
- `@nestjs/typeorm` + `typeorm` + `pg` — TypeORM + PostgreSQL
- `@nestjs/prisma` + `prisma` — Prisma ORM (or `nestjs-prisma` community package)
- `drizzle-orm` + `drizzle-nestjs` — Drizzle ORM
- `@nestjs/passport` + `passport` + `passport-jwt` + `@nestjs/jwt` — JWT auth
- `@nestjs/swagger` — Swagger/OpenAPI generation
- `@nestjs/config` — Typed configuration with env validation
- `@nestjs/throttler` — rate limiting
- `@nestjs/cache-manager` + `cache-manager` — caching (Redis via `cache-manager-redis-yet`)
- `@nestjs/bull` + `bull` — background jobs (Redis-backed queue)
- `@nestjs/schedule` — cron jobs and scheduled tasks
- `@nestjs/websockets` + `@nestjs/platform-socket.io` — WebSocket gateways
- `@nestjs/microservices` — microservice patterns (TCP, Redis, NATS, RabbitMQ transports)
- `@nestjs/graphql` + `@nestjs/apollo` + `apollo-server-express` — GraphQL
- `@nestjs/terminus` — health checks
- `class-validator` + `class-transformer` — DTO validation (required for ValidationPipe)
- `nestjs-pino` + `pino` — structured logging (faster than built-in Logger)
- `@nestjs/cls` — continuation-local storage (request-scoped context without REQUEST scope)
- `@golevelup/nestjs-rabbitmq` — RabbitMQ integration
- `@nestjs/axios` — HTTP client (NestJS-flavored Axios)
