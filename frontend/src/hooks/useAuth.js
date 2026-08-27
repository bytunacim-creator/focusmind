import { useState, useCallback } from "react";

/**
 * DEMO_MODE basit rol seçimi. Gerçek kimlik doğrulama kapsam dışı
 * (bkz. docs/ARCHITECTURE_DECISIONS.md AD-5 — iki rollü basit model).
 */
export function useAuth() {
  const [role, setRole] = useState(null); // "participant" | "researcher"
  const [participantId, setParticipantId] = useState(null);

  const loginAsParticipant = useCallback((id) => {
    if (!/^P\d+$/.test(id)) {
      throw new Error("participant_id 'P001' formatında olmalıdır");
    }
    setRole("participant");
    setParticipantId(id);
  }, []);

  const loginAsResearcher = useCallback(() => {
    setRole("researcher");
    setParticipantId(null);
  }, []);

  const logout = useCallback(() => {
    setRole(null);
    setParticipantId(null);
  }, []);

  return {
    role,
    participantId,
    isAuthenticated: role !== null,
    loginAsParticipant,
    loginAsResearcher,
    logout,
    authHeaders: role ? { role, participantId } : null,
  };
}
