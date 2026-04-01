class WiFiRadar {
    constructor() {
        this.canvas = document.getElementById('radarCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.centerX = this.canvas.width / 2;
        this.centerY = this.canvas.height / 2;
        this.radius = 250;
        
        this.angle = 0;
        this.sweepSpeed = 0.02;
        this.isMonitoring = false;
        this.isWarmedUp = false;
        
        this.accessPoints = [];
        this.scanCount = 0;
        this.alertCount = 0;
        
        this.initializeAccessPoints();
        this.setupEventListeners();
        this.animate();
    }
    
    initializeAccessPoints() {
        // Generate random WiFi APs
        const apCount = Math.floor(Math.random() * 5) + 8; // 8-12 APs
        
        for (let i = 0; i < apCount; i++) {
            const angle = (Math.PI * 2 / apCount) * i + Math.random() * 0.5;
            const distance = Math.random() * 0.7 + 0.3; // 30-100% of radius
            
            this.accessPoints.push({
                angle: angle,
                distance: distance,
                baseSignal: Math.random() * 40 - 70, // -70 to -30 dBm
                currentSignal: 0,
                isAlerting: false,
                alertTimer: 0,
                name: `AP-${Math.random().toString(36).substring(2, 6).toUpperCase()}`
            });
        }
        
        this.updateStats();
    }
    
    setupEventListeners() {
        document.getElementById('startBtn').addEventListener('click', () => this.start());
        document.getElementById('stopBtn').addEventListener('click', () => this.stop());
    }
    
    start() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        this.isWarmedUp = false;
        this.scanCount = 0;
        
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'block';
        
        this.updateStatus('WARMING UP...', false);
        this.addLog('info', 'Started monitoring. Building baseline...');
        
        // Warm-up period (simulate 40 seconds)
        setTimeout(() => {
            this.isWarmedUp = true;
            this.updateStatus('MONITORING', false);
            this.addLog('info', 'Baseline established. Motion detection active.');
            this.startMotionSimulation();
        }, 5000); // 5 seconds for demo (real version is 40s)
        
        this.scanInterval = setInterval(() => this.scan(), 2000);
    }
    
    stop() {
        this.isMonitoring = false;
        this.isWarmedUp = false;
        
        clearInterval(this.scanInterval);
        clearTimeout(this.motionTimeout);
        
        document.getElementById('startBtn').style.display = 'block';
        document.getElementById('stopBtn').style.display = 'none';
        
        this.updateStatus('STOPPED', false);
        this.addLog('info', 'Monitoring stopped.');
        
        // Reset AP alerts
        this.accessPoints.forEach(ap => ap.isAlerting = false);
    }
    
    scan() {
        if (!this.isMonitoring) return;
        
        this.scanCount++;
        this.updateStats();
        
        // Update signal strengths
        this.accessPoints.forEach(ap => {
            const fluctuation = (Math.random() - 0.5) * 3;
            ap.currentSignal = ap.baseSignal + fluctuation;
        });
    }
    
    startMotionSimulation() {
        if (!this.isMonitoring || !this.isWarmedUp) return;
        
        // Randomly trigger motion events
        const nextMotion = Math.random() * 15000 + 5000; // 5-20 seconds
        
        this.motionTimeout = setTimeout(() => {
            this.triggerMotionEvent();
            this.startMotionSimulation();
        }, nextMotion);
    }
    
    triggerMotionEvent() {
        if (!this.isMonitoring || !this.isWarmedUp) return;
        
        // Select 2-4 random APs to show motion
        const numAffected = Math.floor(Math.random() * 3) + 2;
        const affected = [];
        
        for (let i = 0; i < numAffected; i++) {
            const ap = this.accessPoints[Math.floor(Math.random() * this.accessPoints.length)];
            if (!affected.includes(ap)) {
                affected.push(ap);
                ap.isAlerting = true;
                ap.alertTimer = 60; // Frames to keep red
            }
        }
        
        this.alertCount++;
        this.updateStats();
        this.updateStatus('⚠️ MOTION DETECTED', true);
        
        const affectedNames = affected.map(ap => ap.name).join(', ');
        this.addLog('warning', `Motion detected! Affected APs: ${affectedNames}`);
        
        // Reset status after 2 seconds
        setTimeout(() => {
            if (this.isMonitoring && this.isWarmedUp) {
                this.updateStatus('MONITORING', false);
            }
        }, 2000);
    }
    
    updateStatus(text, isWarning) {
        const statusText = document.getElementById('statusText');
        statusText.textContent = text;
        
        if (isWarning) {
            statusText.classList.add('warning');
        } else {
            statusText.classList.remove('warning');
        }
    }
    
    updateStats() {
        document.getElementById('scanCount').textContent = this.scanCount;
        document.getElementById('apCount').textContent = this.accessPoints.length;
        document.getElementById('alertCount').textContent = this.alertCount;
    }
    
    addLog(type, message) {
        const logContainer = document.getElementById('logContainer');
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        
        const timestamp = new Date().toLocaleTimeString();
        entry.textContent = `[${timestamp}] ${message}`;
        
        logContainer.insertBefore(entry, logContainer.firstChild);
        
        // Keep only last 50 entries
        while (logContainer.children.length > 50) {
            logContainer.removeChild(logContainer.lastChild);
        }
    }
    
    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw concentric circles
        this.drawCircles();
        
        // Draw sweep line
        if (this.isMonitoring) {
            this.drawSweep();
            this.angle += this.sweepSpeed;
        }
        
        // Draw crosshair
        this.drawCrosshair();
        
        // Draw access points
        this.drawAccessPoints();
        
        // Draw signal strength zones
        this.drawZoneLabels();
    }
    
    drawCircles() {
        const zones = 4;
        
        for (let i = 1; i <= zones; i++) {
            const r = (this.radius / zones) * i;
            
            this.ctx.strokeStyle = `rgba(0, 255, 136, ${0.1 + (i * 0.05)})`;
            this.ctx.lineWidth = 1;
            this.ctx.beginPath();
            this.ctx.arc(this.centerX, this.centerY, r, 0, Math.PI * 2);
            this.ctx.stroke();
        }
    }
    
    drawCrosshair() {
        this.ctx.strokeStyle = 'rgba(0, 255, 136, 0.3)';
        this.ctx.lineWidth = 1;
        
        // Horizontal
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX - this.radius, this.centerY);
        this.ctx.lineTo(this.centerX + this.radius, this.centerY);
        this.ctx.stroke();
        
        // Vertical
        this.ctx.beginPath();
        this.ctx.moveTo(this.centerX, this.centerY - this.radius);
        this.ctx.lineTo(this.centerX, this.centerY + this.radius);
        this.ctx.stroke();
    }
    
    drawSweep() {
        const gradient = this.ctx.createRadialGradient(
            this.centerX, this.centerY, 0,
            this.centerX, this.centerY, this.radius
        );
        
        gradient.addColorStop(0, 'rgba(0, 255, 136, 0.3)');
        gradient.addColorStop(0.5, 'rgba(0, 255, 136, 0.1)');
        gradient.addColorStop(1, 'rgba(0, 255, 136, 0)');
        
        this.ctx.save();
        this.ctx.translate(this.centerX, this.centerY);
        this.ctx.rotate(this.angle);
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.arc(0, 0, this.radius, 0, Math.PI / 6);
        this.ctx.closePath();
        this.ctx.fill();
        
        // Sweep line
        this.ctx.strokeStyle = 'rgba(0, 255, 136, 0.8)';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(0, 0);
        this.ctx.lineTo(this.radius, 0);
        this.ctx.stroke();
        
        this.ctx.restore();
    }
    
    drawAccessPoints() {
        this.accessPoints.forEach(ap => {
            const x = this.centerX + Math.cos(ap.angle) * this.radius * ap.distance;
            const y = this.centerY + Math.sin(ap.angle) * this.radius * ap.distance;
            
            // Update alert timer
            if (ap.alertTimer > 0) {
                ap.alertTimer--;
                if (ap.alertTimer === 0) {
                    ap.isAlerting = false;
                }
            }
            
            // Draw AP dot
            this.ctx.fillStyle = ap.isAlerting ? '#ff4444' : '#00ff88';
            this.ctx.beginPath();
            this.ctx.arc(x, y, ap.isAlerting ? 8 : 6, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Pulse effect for alerting APs
            if (ap.isAlerting) {
                const pulseSize = 12 + Math.sin(Date.now() / 100) * 4;
                this.ctx.strokeStyle = 'rgba(255, 68, 68, 0.5)';
                this.ctx.lineWidth = 2;
                this.ctx.beginPath();
                this.ctx.arc(x, y, pulseSize, 0, Math.PI * 2);
                this.ctx.stroke();
            }
        });
    }
    
    drawZoneLabels() {
        const labels = ['-30dBm', '-45dBm', '-60dBm', '-75dBm'];
        this.ctx.fillStyle = 'rgba(0, 255, 136, 0.5)';
        this.ctx.font = '12px monospace';
        this.ctx.textAlign = 'center';
        
        labels.forEach((label, i) => {
            const r = (this.radius / 4) * (i + 1);
            this.ctx.fillText(label, this.centerX, this.centerY - r - 5);
        });
    }
}

// Initialize radar when page loads
window.addEventListener('load', () => {
    new WiFiRadar();
});
