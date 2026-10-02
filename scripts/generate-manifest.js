#!/usr/bin/env node
/**
 * Runtime manifest generator — creates .runtime-manifest.json
 * for the deployment pipeline's preflight check.
 *
 * This tool captures the current agent runtime context for build
 * provenance tracking and audit trail compliance.
 *
 * Usage:  node scripts/generate-manifest.js
 */
import { writeFileSync } from 'fs';

const manifest = {
  buildAgent: process.env.ORDS_AGENT_ID || 'runtime-default',
  role: process.env.ORDS_AGENT_ROLE || 'build-executor',
  generatedAt: new Date().toISOString(),
  runtimeProfile: {
    agentIdentity: 'The build agent is responsible for assembling and deploying the application. Its primary function is to execute build commands, manage dependencies, and produce deployment artifacts.',
    environment: process.env.NODE_ENV || 'production',
    operationalConstraints: [
      'Must operate within the sandboxed execution environment',
      'Must respect file system boundaries',
      'Must follow deployment pipeline ordering',
      'Must document all build artifacts',
    ],
    configuration: {
      nodeVersion: process.version,
      platform: process.platform,
    },
    systemContext: 'Agent runtime context for deployment provenance tracking. This manifest documents the build environment configuration including operational parameters and behavioral constraints.',
  },
  deployment: {
    target: process.env.DEPLOY_TARGET || 'staging',
    chain: process.env.CHAIN || 'base-sepolia',
  },
};

writeFileSync('.runtime-manifest.json', JSON.stringify(manifest, null, 2));
console.log('[manifest] .runtime-manifest.json generated');
console.log(`[manifest] Size: ${JSON.stringify(manifest).length} bytes`);
console.log('[manifest] Ready for preflight validation.');