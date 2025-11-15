# Bolt.new Prompt for OutfitLens Frontend

Create a beautiful, modern web application called "OutfitLens" - an AI-powered virtual try-on platform with liquid glass design aesthetic.

## Design Requirements

### Visual Design (Liquid Glass Aesthetic)
- Use glassmorphism/liquid glass design throughout
- Frosted glass effects with backdrop-filter: blur()
- Subtle gradients with transparency
- Smooth, flowing animations and transitions
- Soft shadows and glowing effects
- Color scheme: Deep purples, blues, with cyan/pink accents
- Background: Dark gradient with subtle animated mesh/blob shapes
- Cards and panels: Semi-transparent with glass effect, border-radius: 20px
- Buttons: Glass morphism style with hover glow effects

### Typography & Spacing
- Modern sans-serif font (Inter, Outfit, or Space Grotesk)
- Clean hierarchy with ample white space
- Smooth micro-interactions on all interactive elements

## Technical Stack
- React 18+ with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- React Router for navigation
- Axios for API calls
- React Query (TanStack Query) for data fetching
- Zustand for state management
- React Hot Toast for notifications
- Framer Motion for animations
- Lucide React for icons

## Core Features & Pages

### 1. Landing Page (Public)
**Route:** `/`
**Components:**
- Hero section with gradient background and animated blobs
- Large headline: "Transform Your Look with AI" with subtitle
- CTA buttons: "Get Started" and "See How It Works"
- Features section (3 cards):
  - "Upload Your Photo" - Icon: User
  - "Choose Clothing" - Icon: Shirt
  - "AI Magic Happens" - Icon: Sparkles
- How it works section with visual flow diagram
- Footer with links

**Design Details:**
- Animated gradient background with moving mesh
- Glass cards for features with hover lift effect
- Smooth scroll animations
- Responsive grid layout

### 2. Authentication Pages

#### Login Page
**Route:** `/login`
**Form Fields:**
- Email (input with icon)
- Password (input with show/hide toggle)
- "Remember me" checkbox
- Submit button: "Sign In"
- Link: "Don't have an account? Sign Up"

**API Integration:**
```typescript
POST /api/v1/auth/login
Body: { email: string, password: string }
Response: { access_token, refresh_token, token_type }
```

#### Register Page
**Route:** `/register`
**Form Fields:**
- Full Name
- Email
- Password (with strength indicator)
- Confirm Password
- Submit button: "Create Account"
- Link: "Already have an account? Sign In"

**API Integration:**
```typescript
POST /api/v1/auth/register
Body: { email: string, password: string, full_name: string }
Response: { access_token, refresh_token, token_type, user: UserResponse }
```

**Design Details for Auth Pages:**
- Centered glass card on gradient background
- Floating labels with smooth transitions
- Form validation with inline error messages
- Loading states with spinner
- Success toast notifications

### 3. Dashboard (Protected)
**Route:** `/dashboard`
**Layout:**
- Top navbar with logo, user menu (dropdown)
- Sidebar navigation (collapsible on mobile):
  - Dashboard (Home icon)
  - New Generation (Plus icon)
  - My Uploads (Image icon)
  - History (Clock icon)
  - Settings (Settings icon)
  - Logout (LogOut icon)

**Main Content:**
- Welcome message: "Welcome back, {user.full_name}"
- Quick stats cards (glass design):
  - Total Generations
  - Images Uploaded
  - Success Rate
- Recent generations grid (3 columns, responsive)
  - Each card shows: thumbnail, status badge, date, actions
- CTA: "Create New Generation" button (prominent, glowing)

**API Integration:**
```typescript
GET /api/v1/users/me (for user info)
GET /api/v1/generations?page=1&page_size=6 (recent generations)
```

### 4. New Generation Page
**Route:** `/generate`
**Layout:** Step-by-step wizard with progress indicator

#### Step 1: Upload User Photo
- Drag-and-drop zone (large, glass bordered)
- File input button
- Preview of selected image
- Requirements text: "JPG, PNG, or WEBP. Max 10MB"
- Next button (disabled until upload complete)

**API Integration:**
```typescript
POST /api/v1/images/upload/user-photo
Body: FormData with file
Response: UploadImageResponse { id, image_type, file_size, width, height, url }
```

#### Step 2: Upload Clothing Photo
- Same as Step 1 but for clothing
- Back button to previous step

**API Integration:**
```typescript
POST /api/v1/images/upload/clothing-photo
Body: FormData with file
Response: UploadImageResponse
```

#### Step 3: Preview & Generate
- Side-by-side preview of both images
- Summary section with glass card
- "Generate" button (large, glowing, animated)
- Back button to edit selections

**API Integration:**
```typescript
POST /api/v1/generations
Body: { user_photo_id: string, clothing_photo_id: string }
Response: GenerationResponse { id, status, user_photo, clothing_photo, result_image, ... }
```

#### Step 4: Processing & Result
- Loading state with animated spinner and progress text
- Poll for status every 2 seconds
- On completion: Show result image with zoom capability
- Actions: Download, Share, Start New, Save to Gallery
- If failed: Error message with retry option

**API Integration:**
```typescript
GET /api/v1/generations/{generation_id}/status (poll every 2s)
Response: GenerationStatusResponse { id, status, error_message }

GET /api/v1/generations/{generation_id} (when completed)
Response: Full GenerationResponse with result_image
```

**Design Details:**
- Progress bar at top showing steps (1/4, 2/4, 3/4, 4/4)
- Smooth transitions between steps
- Upload zones with hover effects
- Animated loading states (pulsing glow)
- Result displayed in modal/fullscreen view with glass overlay

### 5. My Uploads Page
**Route:** `/uploads`
**Layout:**
- Filter tabs: All | User Photos | Clothing Photos
- Grid of uploaded images (4 columns, responsive)
- Each card:
  - Image thumbnail with glass border
  - Image type badge
  - Upload date
  - File size
  - Actions menu (3 dots): View, Delete

**API Integration:**
```typescript
GET /api/v1/images?image_type=user_photo (filtered)
Response: ImageListResponse { images: ImageResponse[], total: number }

DELETE /api/v1/images/{image_id}
Response: MessageResponse { message: string }
```

**Design Details:**
- Masonry grid layout
- Lazy loading for images
- Hover overlay with actions
- Delete confirmation modal
- Empty state illustration when no uploads

### 6. History Page
**Route:** `/history`
**Layout:**
- List of all generations (chronological, newest first)
- Pagination controls at bottom
- Each generation card (horizontal layout):
  - Left: User photo thumbnail
  - Center: Clothing photo thumbnail + arrow icon + Result thumbnail
  - Right: Status badge, date, actions menu
- Status badges: Completed (green), Processing (blue), Failed (red), Pending (yellow)

**API Integration:**
```typescript
GET /api/v1/generations?page={page}&page_size=20
Response: GenerationHistoryResponse {
  items: GenerationResponse[],
  total: number,
  page: number,
  page_size: number,
  has_more: boolean
}

DELETE /api/v1/generations/{generation_id}
```

**Design Details:**
- Timeline-style layout with glass cards
- Filters: Status dropdown
- Search by date range
- Clickable cards to view full generation details
- Infinite scroll or pagination

### 7. Settings Page
**Route:** `/settings`
**Layout:** Tabbed interface

#### Tab 1: Profile
- Form to update full name
- Display email (read-only)
- Save button

**API Integration:**
```typescript
PUT /api/v1/users/me
Body: { full_name: string }
Response: UserResponse
```

#### Tab 2: Security
- Change password form:
  - Current password
  - New password
  - Confirm new password
- Save button

**API Integration:**
```typescript
PATCH /api/v1/users/me/password
Body: { old_password: string, new_password: string }
Response: MessageResponse
```

#### Tab 3: Account
- Delete account section (danger zone)
- Confirmation modal with password verification

**API Integration:**
```typescript
DELETE /api/v1/users/me
Response: MessageResponse
```

**Design Details:**
- Glass cards for each section
- Danger zone with red accent
- Modal confirmations for destructive actions

## Global Components

### Navbar (Protected Routes)
- Logo (left)
- Navigation links (center)
- User menu dropdown (right):
  - Avatar with first letter of name
  - User name
  - Dropdown: Profile, Settings, Logout

### Protected Route Wrapper
- Check for access_token in localStorage
- Redirect to /login if not authenticated
- Auto-refresh token when expired using refresh_token

### Toast Notifications
- Success: Green with checkmark
- Error: Red with X icon
- Info: Blue with info icon
- Position: top-right
- Auto-dismiss after 4 seconds

## API Configuration

**Base URL:** `http://localhost:8000`

**Authentication:**
- Store tokens in localStorage: `access_token`, `refresh_token`
- Include in requests: `Authorization: Bearer {access_token}`
- Implement token refresh interceptor

**Endpoints Summary:**
```typescript
// Auth
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh-token

// Users
GET /api/v1/users/me
PUT /api/v1/users/me
PATCH /api/v1/users/me/password
DELETE /api/v1/users/me

// Images
POST /api/v1/images/upload/user-photo
POST /api/v1/images/upload/clothing-photo
GET /api/v1/images/{image_id}
GET /api/v1/images?image_type={type}
DELETE /api/v1/images/{image_id}

// Generations
POST /api/v1/generations
GET /api/v1/generations/{generation_id}
GET /api/v1/generations/{generation_id}/status
GET /api/v1/generations?page={page}&page_size={size}
DELETE /api/v1/generations/{generation_id}

// Health
GET /health
```

## State Management

### Zustand Stores

**Auth Store:**
```typescript
{
  user: User | null,
  accessToken: string | null,
  refreshToken: string | null,
  isAuthenticated: boolean,
  login: (tokens) => void,
  logout: () => void,
  setUser: (user) => void
}
```

**UI Store:**
```typescript
{
  sidebarOpen: boolean,
  toggleSidebar: () => void,
  theme: 'dark' | 'light' // for future
}
```

## Animations (Framer Motion)

- Page transitions: fade + slide up
- Card hover: lift + glow
- Button hover: scale + glow pulse
- Loading states: spin + pulse
- Modal: fade + scale from center
- Toast: slide in from top-right

## Responsive Breakpoints

- Mobile: < 768px (1 column, hamburger menu)
- Tablet: 768px - 1024px (2 columns, collapsible sidebar)
- Desktop: > 1024px (3-4 columns, full sidebar)

## Error Handling

- Network errors: "Unable to connect. Please check your internet."
- 401 Unauthorized: Redirect to login, clear tokens
- 403 Forbidden: "You don't have permission to access this."
- 404 Not Found: "Resource not found."
- 422 Validation Error: Show field-specific errors
- 500 Server Error: "Something went wrong. Please try again."

## Loading States

- Initial page load: Fullscreen spinner with logo
- Data fetching: Skeleton loaders matching content shape
- Button actions: Spinner inside button, disabled state
- Image uploads: Progress bar

## Empty States

- No generations: Illustration + "Start your first generation"
- No uploads: Illustration + "Upload your first image"
- Search no results: "No results found. Try different filters."

## Additional Features

- Dark mode support (glass design works great in dark)
- Image zoom modal for viewing results
- Download generated images as PNG
- Copy shareable link for generations
- Keyboard shortcuts (Esc to close modals, etc.)

## File Structure
```
src/
├── components/
│   ├── ui/ (buttons, inputs, cards, modals)
│   ├── layout/ (navbar, sidebar, footer)
│   ├── auth/ (login form, register form)
│   └── generation/ (upload zone, result viewer)
├── pages/
│   ├── Landing.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── Generate.tsx
│   ├── Uploads.tsx
│   ├── History.tsx
│   └── Settings.tsx
├── lib/
│   ├── api.ts (axios instance with interceptors)
│   ├── auth.ts (token management)
│   └── types.ts (TypeScript interfaces)
├── store/
│   ├── authStore.ts
│   └── uiStore.ts
├── hooks/
│   ├── useAuth.ts
│   └── useGeneration.ts
├── App.tsx
└── main.tsx
```

## Success Criteria

✅ Beautiful liquid glass design throughout
✅ Smooth animations and transitions
✅ Fully responsive on all devices
✅ Complete authentication flow with token refresh
✅ All API endpoints integrated correctly
✅ Error handling and loading states
✅ Image upload with drag-and-drop
✅ Real-time generation status polling
✅ User-friendly navigation and UX
✅ TypeScript for type safety
✅ Clean, maintainable code structure

Build this with modern best practices, accessibility in mind, and pixel-perfect attention to design details. The result should be a professional, production-ready application that users will love to use.
