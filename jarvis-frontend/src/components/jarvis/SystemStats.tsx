import { useState, useEffect } from "react";
import { Cpu, HardDrive, Wifi, Zap, Battery, BatteryCharging } from "lucide-react";
import { useSystemStatus } from "@/hooks/use-system-status";
import { getSystemStats, SystemStatsResponse } from "@/services/api";

interface StatItemProps {
  icon: React.ReactNode;
  label: string;
  value: number;
  unit?: string;
  color?: string;
  subtext?: string;
}

const StatItem = ({ icon, label, value, unit = "%", subtext }: StatItemProps) => (
  <div className="space-y-2">
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-[10px] text-muted-foreground">
        {icon}
        <span className="uppercase tracking-wider">{label}</span>
      </div>
      <div className="text-[10px] text-primary tabular-nums">
        {value.toFixed(0)}{unit}
        {subtext && <span className="text-muted-foreground ml-1">{subtext}</span>}
      </div>
    </div>
    <div className="relative h-1.5 bg-muted/30 rounded-full overflow-hidden">
      <div 
        className="absolute inset-y-0 left-0 rounded-full transition-all duration-1000"
        style={{ 
          width: `${Math.min(value, 100)}%`,
          background: value > 80 
            ? "linear-gradient(90deg, hsl(0 80% 50%), hsl(30 100% 50%))" 
            : "linear-gradient(90deg, hsl(195 100% 55%), hsl(210 100% 70%))",
          boxShadow: value > 80 
            ? "0 0 10px hsl(0 80% 50% / 0.5)"
            : "0 0 10px hsl(195 100% 55% / 0.5)"
        }}
      />
    </div>
  </div>
);

const SystemStats = () => {
  const systemStatus = useSystemStatus(10000); // Check every 10 seconds
  const [stats, setStats] = useState<{
    cpu: number;
    memory: number;
    disk: number;
    battery: number | null;
    batteryCharging: boolean;
    memoryUsed: number;
    memoryTotal: number;
  }>({
    cpu: 0,
    memory: 0,
    disk: 0,
    battery: null,
    batteryCharging: false,
    memoryUsed: 0,
    memoryTotal: 0,
  });

  useEffect(() => {
    // Fetch real system stats from backend
    const fetchStats = async () => {
      if (!systemStatus.isConnected) return;
      
      try {
        const data = await getSystemStats();
        if (data.success) {
          setStats({
            cpu: data.cpu?.percent || 0,
            memory: data.memory?.percent || 0,
            disk: data.disk?.percent || 0,
            battery: data.battery?.percent ?? null,
            batteryCharging: data.battery?.charging || false,
            memoryUsed: data.memory?.used_gb || 0,
            memoryTotal: data.memory?.total_gb || 0,
          });
        }
      } catch (error) {
        console.error('Failed to fetch system stats:', error);
      }
    };

    // Fetch immediately and then every 2 seconds
    fetchStats();
    const interval = setInterval(fetchStats, 2000);

    return () => clearInterval(interval);
  }, [systemStatus.isConnected]);

  return (
    <div className="holo-panel p-4 space-y-4">
      <div className="flex items-center justify-between border-b border-primary/20 pb-2">
        <h3 className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">
          System Status
        </h3>
        <div className="flex items-center gap-1">
          <div className={`w-1.5 h-1.5 rounded-full ${systemStatus.isConnected ? 'bg-primary animate-pulse' : 'bg-red-500'}`} />
          <span className={`text-[8px] ${systemStatus.isConnected ? 'text-primary/60' : 'text-red-500/60'}`}>
            {systemStatus.isConnected ? 'LIVE' : 'OFFLINE'}
          </span>
        </div>
      </div>
      
      <StatItem 
        icon={<Cpu className="w-3 h-3" />} 
        label="CPU" 
        value={stats.cpu} 
      />
      
      <StatItem 
        icon={<HardDrive className="w-3 h-3" />} 
        label="RAM" 
        value={stats.memory}
        subtext={`${stats.memoryUsed}/${stats.memoryTotal}GB`}
      />
      
      <StatItem 
        icon={<Wifi className="w-3 h-3" />} 
        label="Disk" 
        value={stats.disk} 
      />
      
      {stats.battery !== null ? (
        <StatItem 
          icon={stats.batteryCharging ? <BatteryCharging className="w-3 h-3" /> : <Battery className="w-3 h-3" />} 
          label={stats.batteryCharging ? "Charging" : "Battery"} 
          value={stats.battery} 
        />
      ) : (
        <StatItem 
          icon={<Zap className="w-3 h-3" />} 
          label="Arc Power" 
          value={100} 
        />
      )}

      {/* Mini reactor indicator */}
      <div className="flex items-center justify-center pt-2 border-t border-primary/20">
        <div className="relative">
          <div 
            className="w-8 h-8 rounded-full animate-reactor-pulse"
            style={{
              background: systemStatus.isConnected 
                ? "radial-gradient(circle, hsl(195 100% 80%) 0%, hsl(195 100% 50%) 50%, transparent 70%)"
                : "radial-gradient(circle, hsl(0 50% 50%) 0%, hsl(0 50% 30%) 50%, transparent 70%)"
            }}
          />
          <div className="absolute inset-0 w-8 h-8 rounded-full border border-primary/30" />
        </div>
      </div>
    </div>
  );
};

export default SystemStats;