import {defineConfig, devices} from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  reporter: 'html',

  use:{
    baseURL: 'http://127.0.0.1:5000',
    trace: 'on-first-retry',
  },
  workers: 4,
  projects:[
    {
      name: 'auth-tests',
      testMatch: /.*auth\.test\.ts/,
      use: {...devices['Desktop Chrome']},
    },
    {
      name: 'chromium', 
      use: {...devices['Desktop Chrome']},
      testIgnore: /.*auth\.test\.ts/,
    },
  ],

  webServer:{
    command: 'python3 ../Visionsofme/app.py',
    url: 'http://127.0.0.1:5000',
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});