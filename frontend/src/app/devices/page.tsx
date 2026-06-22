import {
  DevicesDashboardClient,
  type Device,
} from "@/components/devices-dashboard-client";

export const dynamic = "force-dynamic";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type DevicesResult = {
  devices: Device[];
  error: string | null;
};

async function getInitialDevices(): Promise<DevicesResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/devices`, { cache: "no-store" });
    if (!response.ok) {
      return {
        devices: [],
        error: `Backend returned ${response.status}. Check API at ${API_BASE_URL}.`,
      };
    }

    return { devices: (await response.json()) as Device[], error: null };
  } catch {
    return {
      devices: [],
      error: `Could not connect to backend at ${API_BASE_URL}. Start FastAPI server and try again.`,
    };
  }
}

export default async function Page() {
  const { devices, error } = await getInitialDevices();

  return (
    <DevicesDashboardClient
      initialDevices={devices}
      initialError={error}
      apiBaseUrl={API_BASE_URL}
    />
  );
}
