type Device = {
  id: string;
  device_type: string;
};

export const dynamic = "force-dynamic";

type DevicesResult = {
  devices: Device[];
  error: string | null;
};

async function getDevices(): Promise<DevicesResult> {
  const apiBaseUrl =
    process.env.NEXT_PUBLIC_API_URL ?? process.env.API_URL ?? "http://127.0.0.1:8000";

  try {
    const response = await fetch(`${apiBaseUrl}/devices`, { cache: "no-store" });
    if (!response.ok) {
      return {
        devices: [],
        error: `Backend returned ${response.status}. Check API at ${apiBaseUrl}.`,
      };
    }

    return { devices: (await response.json()) as Device[], error: null };
  } catch {
    return {
      devices: [],
      error: `Could not connect to backend at ${apiBaseUrl}. Start FastAPI server and try again.`,
    };
  }
}

export default async function Page() {
  const { devices, error } = await getDevices();

  return (
    <div className="space-y-3">
      <h1 className="text-xl font-semibold">Devices</h1>
      {error ? (
        <div className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-800">
          {error}
        </div>
      ) : null}
      <pre className="rounded-md border p-3 text-sm">
        {JSON.stringify(devices, null, 2)}
      </pre>
    </div>
  );
}
