"use client";

import { useMemo, useState } from "react";

export type Device = {
  id: string;
  name: string;
  device_type: string;
  state: string;
  cpu: number;
  memory: number;
  battery: number;
  trust_score: number;
  created_at: string;
};

type DevicesDashboardClientProps = {
  initialDevices: Device[];
  initialError: string | null;
  apiBaseUrl: string;
};

export function DevicesDashboardClient({
  initialDevices,
  initialError,
  apiBaseUrl,
}: DevicesDashboardClientProps) {
  const [devices, setDevices] = useState<Device[]>(initialDevices);
  const [error, setError] = useState<string | null>(initialError);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const fetchDevices = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/devices`, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }
      const payload = (await response.json()) as Device[];
      setDevices(payload);
    } catch {
      setDevices([]);
      setError(`Could not fetch devices from ${apiBaseUrl}. Ensure backend is running.`);
    } finally {
      setLoading(false);
    }
  };

  const createSimulation = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/simulation/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ device_count: 1000 }),
      });

      if (!response.ok) {
        throw new Error(`Simulation create failed with ${response.status}`);
      }

      await fetchDevices();
    } catch {
      setError(`Failed to create simulation. Check backend at ${apiBaseUrl}.`);
    } finally {
      setSubmitting(false);
    }
  };

  const deleteSimulation = async () => {
    setSubmitting(true);
    setError(null);
    try {
      const response = await fetch(`${apiBaseUrl}/simulation`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Simulation delete failed with ${response.status}`);
      }

      await fetchDevices();
    } catch {
      setError(`Failed to delete simulation. Check backend at ${apiBaseUrl}.`);
    } finally {
      setSubmitting(false);
    }
  };

  const summary = useMemo(() => {
    const total = devices.length;
    const healthy = devices.filter((device) => device.state === "healthy").length;
    const avgTrust =
      total === 0
        ? 0
        : devices.reduce((acc, device) => acc + device.trust_score, 0) / total;
    const typeSet = new Set(devices.map((device) => device.device_type));

    return {
      total,
      healthy,
      avgTrust: Number(avgTrust.toFixed(2)),
      types: typeSet.size,
    };
  }, [devices]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold">Devices</h1>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => void createSimulation()}
            disabled={submitting}
            className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
          >
            {submitting ? "Working..." : "Generate Simulation"}
          </button>
          <button
            type="button"
            onClick={() => void deleteSimulation()}
            disabled={submitting}
            className="rounded-md border px-4 py-2 text-sm font-medium disabled:opacity-50"
          >
            Clear Simulation
          </button>
        </div>
      </div>

      {error ? (
        <div className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-800">
          {error}
        </div>
      ) : null}

      <div className="grid gap-3 md:grid-cols-4">
        <SummaryCard label="Total Devices" value={summary.total.toString()} />
        <SummaryCard label="Healthy Devices" value={summary.healthy.toString()} />
        <SummaryCard label="Average Trust" value={summary.avgTrust.toString()} />
        <SummaryCard label="Device Types" value={summary.types.toString()} />
      </div>

      <div className="overflow-x-auto rounded-md border">
        <table className="min-w-full divide-y">
          <thead className="bg-muted/40">
            <tr className="text-left text-sm">
              <th className="px-3 py-2 font-medium">Name</th>
              <th className="px-3 py-2 font-medium">Type</th>
              <th className="px-3 py-2 font-medium">State</th>
              <th className="px-3 py-2 font-medium">CPU</th>
              <th className="px-3 py-2 font-medium">Memory</th>
              <th className="px-3 py-2 font-medium">Battery</th>
              <th className="px-3 py-2 font-medium">Trust</th>
            </tr>
          </thead>
          <tbody className="divide-y text-sm">
            {devices.map((device) => (
              <tr key={device.id}>
                <td className="px-3 py-2">{device.name}</td>
                <td className="px-3 py-2">{device.device_type}</td>
                <td className="px-3 py-2">{device.state}</td>
                <td className="px-3 py-2">{device.cpu}</td>
                <td className="px-3 py-2">{device.memory}</td>
                <td className="px-3 py-2">{device.battery}</td>
                <td className="px-3 py-2">{device.trust_score}</td>
              </tr>
            ))}
            {devices.length === 0 && !loading ? (
              <tr>
                <td colSpan={7} className="px-3 py-6 text-center text-muted-foreground">
                  No devices found. Click Generate Simulation to create 1000 devices.
                </td>
              </tr>
            ) : null}
            {loading ? (
              <tr>
                <td colSpan={7} className="px-3 py-6 text-center text-muted-foreground">
                  Loading devices...
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function SummaryCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border p-4">
      <p className="text-sm text-muted-foreground">{label}</p>
      <p className="mt-1 text-2xl font-semibold">{value}</p>
    </div>
  );
}
