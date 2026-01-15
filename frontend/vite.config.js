import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0', // Allow connections from outside the container
    port: 3000,
    strictPort: true, // Recommended to avoid silent port shifts
  }
  // ... rest of your config
})

//export default defineConfig({
//  plugins: [react()],
//})
