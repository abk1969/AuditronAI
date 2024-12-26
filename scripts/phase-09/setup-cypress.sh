#!/bin/bash
set -e

echo "🌲 Configuration de Cypress..."

# Installer Cypress
cd frontend
npm install cypress @testing-library/cypress @cypress/code-coverage

# Configuration de Cypress
cat > cypress.config.ts << EOF
import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    supportFile: 'cypress/support/e2e.ts',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    experimentalStudio: true
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite'
    }
  }
})
EOF

# Structure des tests Cypress
mkdir -p cypress/{e2e,fixtures,support,component}

# Tests E2E de base
cat > cypress/e2e/auth.cy.ts << EOF
describe('Authentication', () => {
  beforeEach(() => {
    cy.visit('/auth')
  })

  it('should login successfully', () => {
    cy.get('[data-testid=email-input]').type('test@example.com')
    cy.get('[data-testid=password-input]').type('password123')
    cy.get('[data-testid=login-button]').click()
    cy.url().should('include', '/dashboard')
  })

  it('should show error on invalid credentials', () => {
    cy.get('[data-testid=email-input]').type('invalid@example.com')
    cy.get('[data-testid=password-input]').type('wrongpass')
    cy.get('[data-testid=login-button]').click()
    cy.get('[data-testid=error-message]').should('be.visible')
  })
})
EOF

echo "✅ Cypress configuré avec succès" 