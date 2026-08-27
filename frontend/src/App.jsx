import { useAuth } from "./hooks/useAuth.js";
import DemoBanner from "./components/DemoBanner.jsx";
import RoleSelect from "./pages/RoleSelect.jsx";
import ParticipantFlow from "./pages/ParticipantFlow.jsx";
import ResearcherDashboard from "./pages/ResearcherDashboard.jsx";

export default function App() {
  const auth = useAuth();

  return (
    <div>
      <DemoBanner />
      {auth.isAuthenticated && (
        <div style={{ textAlign: "right", padding: 8 }}>
          <button onClick={auth.logout}>Çıkış</button>
        </div>
      )}

      {!auth.isAuthenticated && (
        <RoleSelect
          onParticipant={auth.loginAsParticipant}
          onResearcher={auth.loginAsResearcher}
        />
      )}

      {auth.isAuthenticated && auth.role === "participant" && (
        <ParticipantFlow auth={auth.authHeaders} />
      )}

      {auth.isAuthenticated && auth.role === "researcher" && (
        <ResearcherDashboard auth={auth.authHeaders} />
      )}
    </div>
  );
}
