import { useAuth0 } from "@auth0/auth0-react";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <button onClick={() => logout({
      logoutParams: {
        returnTo: typeof window !== 'undefined' ? window.location.origin : undefined
      }
    })}>
      Sair
    </button>
  );
};

export default LogoutButton;
