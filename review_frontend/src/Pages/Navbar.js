/**
 * @fileoverview Navigation Bar component using Material-UI
 * Provides responsive navigation with authentication-aware menu items
 */

import * as React from "react";
import { useNavigate } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";

/**
 * NavBar component for application navigation
 * @component
 * @param {Object} _props - Component props
 * @param {Function} props.navigation - Navigation function for routing
 * @returns {JSX.Element} Rendered NavBar component
 */
function NavBar(_props) {
  const navigate = useNavigate();
  /**
   * Dynamic navigation menu items based on authentication state
   * @type {Array<string>}
   */
  let pages = ["Home", "Login", "Signup"];

  // Modify navigation options if user is logged in
  if (localStorage.getItem("login") === "true") {
    pages = ["Home", "Add Review", "View Reviews", "Logout"];
  }

  /**
   * State for mobile menu anchor element
   * @type {[HTMLElement | null, Function]}
   */
  const [anchorElNav, setAnchorElNav] = React.useState(null);

  /**
   * Handles opening the mobile navigation menu
   * @param {React.MouseEvent<HTMLElement>} event - Click event
   */
  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  /**
   * Handles closing the mobile navigation menu
   * @param {React.KeyboardEvent<HTMLElement>} e - Keyboard event
   */
  const handleCloseNavMenu = (e) => {
    console.log(e.key);
  };

  /**
   * Handles navigation to different pages
   * @param {string} page - Page name to navigate to
   * @description Routes to appropriate page and handles logout functionality
   */
  const goto = (page) => {
    if (page === "Home") {
      navigate("/");
    } else if (page === "Login") {
      navigate("/login");
    } else if (page === "Signup") {
      navigate("/signup");
    } else if (page === "Logout") {
      localStorage.setItem("login", "false");
      navigate("/");
    } else if (page === "Add Review") {
      navigate("/add-review");
    } else if (page === "View Reviews") {
      navigate("/view-reviews");
    }
  };

  return (
    <AppBar position="static" color="black">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Desktop Title */}
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#"
            sx={{
              mr: 2,
              display: { xs: "none", md: "flex" },
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "inherit",
              textDecoration: "none",
            }}
          >
            NCSU CAMPUS JOB REVIEW
          </Typography>

          {/* Mobile Navigation Menu */}
          <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
            <IconButton
              size="large"
              aria-label="navigation menu"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{ display: { xs: "block", md: "none" } }}
            >
              {/* Mobile Menu Items */}
              {pages.map((page) => (
                <MenuItem key={page} onClick={() => goto(page)}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>

          {/* Mobile Title */}
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="#"
            sx={{
              mr: 2,
              display: { xs: "flex", md: "none" },
              flexGrow: 1,
              fontFamily: "monospace",
              fontWeight: 700,
              letterSpacing: ".3rem",
              color: "inherit",
              textDecoration: "none",
            }}
          >
            NCSU CAMPUS JOB REVIEW
          </Typography>

          {/* Desktop Navigation Buttons */}
          <Box
            sx={{ flexGrow: 1, display: "flex", justifyContent: "flex-end" }}
          >
            {pages.map((page) => (
              <Button
                key={page}
                onClick={() => goto(page)}
                sx={{ my: 2, color: "grey", display: "block" }}
                aria-label={`Navigate to ${page}`}
              >
                {page}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default NavBar;
