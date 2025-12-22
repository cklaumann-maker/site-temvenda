module.exports = {
  apps: [{
    name: 'rotina-app',
    script: 'node_modules/next/dist/bin/next',
    args: 'start -p 3001',
    cwd: '/var/www/rotina-app/apps/web',
    instances: 1,
    exec_mode: 'fork',
    env: {
      NODE_ENV: 'production',
      PORT: 3001
    },
    error_file: '/var/log/rotina-app/error.log',
    out_file: '/var/log/rotina-app/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};

