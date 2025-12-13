# 🧪 AI Resume Optimizer - Complete Testing Guide

This guide provides comprehensive testing procedures for all application flows.

## Prerequisites

- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:5173`
- PostgreSQL database running
- Browser Developer Tools open (F12) to monitor network requests

---

## 1. Authentication Flow Testing

### 1.1 User Registration

**Test Steps:**
1. Navigate to `http://localhost:5173/signup`
2. Fill in the registration form:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Password: `Test123456`
   - Confirm Password: `Test123456`
   - Check "I accept the terms and conditions"
3. Click "Sign Up"
4. Verify success message appears
5. Check browser console for: `Token stored: [token]`
6. Verify redirect to `/login` page

**Expected Results:**
- ✅ Form validates all fields
- ✅ API call to `POST /api/v1/auth/register` succeeds
- ✅ Success message displays
- ✅ Redirects to login page after 2 seconds
- ✅ No errors in console

**API Verification:**
```bash
# Check API response
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"Test123456"}'
```

**Error Cases to Test:**
- ❌ Duplicate email (should show error)
- ❌ Invalid email format (should show validation error)
- ❌ Password < 8 characters (should show error)
- ❌ Passwords don't match (should show error)
- ❌ Terms not accepted (should show error)

---

### 1.2 User Login

**Test Steps:**
1. Navigate to `http://localhost:5173/login`
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `Test123456`
3. Click "Sign In"
4. Monitor network tab for API call
5. Check localStorage: `localStorage.getItem('token')`
6. Verify redirect to `/upload` page

**Expected Results:**
- ✅ API call to `POST /api/v1/auth/login/json` succeeds
- ✅ Response contains `access_token`
- ✅ Token stored in localStorage
- ✅ User redirected to `/upload`
- ✅ Navbar shows user name

**API Verification:**
```bash
# Test login API
curl -X POST http://localhost:8000/api/v1/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123456"}'
```

**Error Cases to Test:**
- ❌ Wrong password (should show "Incorrect email or password")
- ❌ Non-existent email (should show error)
- ❌ Empty fields (should show validation error)

---

### 1.3 Protected Routes

**Test Steps:**
1. **Without Authentication:**
   - Clear localStorage: `localStorage.clear()`
   - Navigate to `http://localhost:5173/dashboard`
   - Should redirect to `/login`
   
2. **With Authentication:**
   - Login successfully
   - Navigate to `/dashboard`
   - Should display dashboard content
   
3. **Logout:**
   - Click logout button
   - Verify token removed from localStorage
   - Verify redirect to home page

**Expected Results:**
- ✅ Unauthenticated users redirected to login
- ✅ Authenticated users can access protected routes
- ✅ Logout clears token and redirects

---

## 2. Resume Upload Flow Testing

### 2.1 File Upload

**Test Steps:**
1. Login and navigate to `/upload`
2. **Valid Upload:**
   - Click or drag & drop a PDF file (< 5MB)
   - Click "Upload Resume"
   - Monitor network tab for `POST /api/v1/resume/upload`
   - Verify success message appears
   - Check `resumeId` is set in state

**Expected Results:**
- ✅ File uploads successfully
- ✅ API returns `resume_id`
- ✅ Success indicator shows
- ✅ File name displayed

**API Verification:**
```bash
# Test upload (requires authentication token)
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@resume.pdf"
```

**Error Cases to Test:**
- ❌ Upload non-PDF/DOCX file (should show error)
- ❌ Upload file > 5MB (should show error)
- ❌ Upload without authentication (should redirect)
- ❌ Upload corrupted file (should show error)

---

### 2.2 File Validation

**Test Cases:**
1. **File Type Validation:**
   - Try uploading `.txt` file → Should reject
   - Try uploading `.jpg` file → Should reject
   - Upload `.pdf` → Should accept
   - Upload `.docx` → Should accept

2. **File Size Validation:**
   - Upload file < 5MB → Should accept
   - Upload file > 5MB → Should show error

---

## 3. Job Description Flow Testing

### 3.1 Job Description Input

**Test Steps:**
1. On `/upload` page, scroll to "Add Job Description" section
2. Enter job details:
   - Job Title: `Senior React Developer` (optional)
   - Company: `Tech Corp` (optional)
   - Job Description: `We are looking for an experienced React developer with 5+ years of experience...` (minimum 10 characters)
3. Click "Save Job Description"
4. Monitor network tab for `POST /api/v1/job/`
5. Verify success message appears

**Expected Results:**
- ✅ Job description saves successfully
- ✅ API returns `job_id`
- ✅ Success indicator shows
- ✅ Character count updates

**Sample Job Description:**
```
We are looking for a Senior React Developer to join our team. 
Requirements:
- 5+ years of React experience
- Strong knowledge of TypeScript
- Experience with Redux
- Familiarity with testing frameworks
- Excellent communication skills
```

**Error Cases to Test:**
- ❌ Description < 10 characters (should show error)
- ❌ Empty description (should disable button)
- ❌ Special characters (should handle properly)

---

## 4. Analysis Flow Testing

### 4.1 Complete Analysis

**Test Steps:**
1. Ensure resume is uploaded (have `resumeId`)
2. Ensure job description is saved (have `jobId`)
3. Click "Analyze Resume" button
4. Monitor network tab for:
   - `POST /api/v1/analysis/analyze`
5. Wait for analysis to complete
6. Verify redirect to `/results/{analysis_id}`
7. Check results page displays:
   - ATS Score (circular progress)
   - Score breakdown
   - Matched skills
   - Missing skills
   - Recommendations

**Expected Results:**
- ✅ Analysis completes successfully
- ✅ ATS score displayed (0-100)
- ✅ All sections populated with data
- ✅ Charts render correctly
- ✅ Recommendations list displayed

**API Verification:**
```bash
# Test analysis (requires resume_id and job_id)
curl -X POST http://localhost:8000/api/v1/analysis/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"resume_id": 1, "job_id": 1}'
```

**Response Structure:**
```json
{
  "id": 1,
  "ats_score": 85.5,
  "score_breakdown": {
    "skills_score": 90,
    "experience_score": 80,
    "keywords_score": 85,
    "format_score": 90
  },
  "matched_skills": ["React", "TypeScript", "Redux"],
  "missing_skills": ["GraphQL", "Docker"],
  "recommendations": [...]
}
```

---

### 4.2 Results Display

**Test Steps:**
1. Navigate to `/results/{id}` after analysis
2. Verify all sections display:
   - **ATS Score Card:** Large circular progress indicator
   - **Score Breakdown:** Progress bars for each category
   - **Skills Analysis:** Two columns (Matched/Missing)
   - **Recommendations:** Prioritized list
   - **Actions:** "Analyze Another" and "View Dashboard" buttons

**Expected Results:**
- ✅ All data displays correctly
- ✅ Score color changes based on value (green/blue/yellow/red)
- ✅ Skills lists are scrollable if long
- ✅ Recommendations expandable
- ✅ Buttons navigate correctly

---

## 5. Dashboard Flow Testing

### 5.1 Dashboard Display

**Test Steps:**
1. Navigate to `/dashboard`
2. Verify displays:
   - Stats cards (Total Analyses, Average Score, Best Score, Improvement)
   - Score trend chart (if analyses exist)
   - Analysis history table
3. Click "View" on any analysis
4. Verify redirects to `/results/{id}`

**Expected Results:**
- ✅ Stats load correctly
- ✅ Chart renders (if data exists)
- ✅ Table displays all analyses
- ✅ Empty state shows if no analyses
- ✅ Navigation works

**API Verification:**
```bash
# Get dashboard stats
curl -X GET http://localhost:8000/api/v1/dashboard/stats \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get analysis history
curl -X GET http://localhost:8000/api/v1/analysis/?limit=20 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 6. Navigation & UI Testing

### 6.1 Navigation Flow

**Test All Navigation Paths:**
1. **Home → Signup → Login → Upload → Results → Dashboard**
   - Home page → Click "Get Started" → Signup page
   - Signup → Click "Sign in" → Login page
   - Login → Redirects to Upload
   - Upload → Analyze → Results page
   - Results → Click "View Dashboard" → Dashboard

2. **Protected Route Access:**
   - Try accessing `/upload` without login → Redirects to `/login`
   - Try accessing `/dashboard` without login → Redirects to `/login`
   - Login → Access protected routes → Should work

3. **Back Navigation:**
   - Results page → Click "Back to Dashboard" → Returns to dashboard
   - Dashboard → Click "New Analysis" → Goes to upload

---

### 6.2 UI Element Testing

**Test All UI Components:**
1. **Buttons:**
   - All buttons visible (not white on white)
   - Hover states work
   - Disabled states show correctly
   - Loading states display spinner

2. **Forms:**
   - Input fields have focus states
   - Validation errors display
   - Placeholders show correctly
   - Icons display in inputs

3. **Cards:**
   - Glass-morphism effect visible
   - Shadows render correctly
   - Borders visible

4. **Icons:**
   - Lucide React icons render
   - Icons have correct colors
   - Icons scale properly

5. **Responsive Design:**
   - Test on mobile viewport (< 768px)
   - Test on tablet viewport (768px - 1024px)
   - Test on desktop viewport (> 1024px)
   - All elements should be accessible

---

## 7. Error Handling Testing

### 7.1 Network Errors

**Test Scenarios:**
1. **Backend Down:**
   - Stop backend server
   - Try to login → Should show network error
   - Error message should be user-friendly

2. **Timeout:**
   - Simulate slow network (Chrome DevTools → Network → Throttling)
   - Try upload → Should timeout after 10 seconds
   - Error message should display

3. **401 Unauthorized:**
   - Use expired token
   - Make API call → Should redirect to login
   - Token should be cleared

---

### 7.2 Validation Errors

**Test All Form Validations:**
1. **Login Form:**
   - Empty email → Shows error
   - Invalid email format → Shows error
   - Empty password → Shows error

2. **Signup Form:**
   - All field validations
   - Password strength
   - Email uniqueness

3. **Upload Form:**
   - File type validation
   - File size validation
   - Required fields

---

## 8. Performance Testing

### 8.1 Load Times

**Test Performance:**
1. **Page Load:**
   - Home page loads < 2 seconds
   - Dashboard loads < 3 seconds
   - Results page loads < 2 seconds

2. **API Response Times:**
   - Login < 1 second
   - Upload < 5 seconds (depends on file size)
   - Analysis < 10 seconds
   - Dashboard stats < 1 second

---

## 9. Browser Compatibility Testing

**Test on Multiple Browsers:**
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (if available)
- ✅ Mobile browsers

---

## 10. Console Error Checking

**Check Browser Console:**
1. Open DevTools (F12)
2. Check Console tab
3. Should see:
   - ✅ No red errors
   - ✅ API calls logged (optional)
   - ✅ Token stored messages (optional)

**Common Issues:**
- ❌ CORS errors → Check backend CORS settings
- ❌ 401 errors → Check token validity
- ❌ 404 errors → Check API endpoints
- ❌ Network errors → Check backend is running

---

## Quick Test Checklist

Use this checklist for quick verification:

- [ ] User can register
- [ ] User can login
- [ ] Token stored in localStorage
- [ ] Protected routes redirect when not authenticated
- [ ] Resume uploads successfully
- [ ] Job description saves
- [ ] Analysis completes and shows results
- [ ] Dashboard displays stats and history
- [ ] All buttons are visible and functional
- [ ] Navigation works correctly
- [ ] Error messages display properly
- [ ] Loading states show during operations
- [ ] Responsive design works on mobile
- [ ] No console errors

---

## Testing Commands

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend
cd frontend
npm run dev

# Run backend tests
cd backend
pytest -v

# Check API health
curl http://localhost:8000/health
```

---

## Notes

- Always test with real PDF/DOCX files
- Use different file sizes to test limits
- Test with various job description lengths
- Monitor network tab for all API calls
- Check localStorage for token storage
- Verify database entries after operations

