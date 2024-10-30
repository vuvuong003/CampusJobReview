import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
// import { useNavigate } from 'react-router-dom';

function NavBar(props) {

  let pages = ['Home', 'Login', 'Signup'];

  // check if localstorage has login key
  if(localStorage.getItem('login') === 'true'){
    pages = ['Home', 'Add Review', 'View Reviews', 'Logout'];
  }

  const [anchorElNav, setAnchorElNav] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = (e) => {
    console.log(e.key)
  };

  const goto = (page) => {
    if(page === "Home"){
        props.navigation('/')
    }else if(page === "Login"){
        props.navigation('/login')
    }else if(page === "Signup"){
        props.navigation('/signup')
    }else if(page === "Logout") {
        localStorage.setItem("login", "false");
        props.navigation('/')
    }else if (page === "Add Review"){
        props.navigation('/add-review')
    }else if (page === "View Reviews"){
        props.navigation('/view-reviews')
    }
  }

//   const navigate = useNavigate();

  return (
    <AppBar position="static" color='black'>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Left-aligned Title */}
          <Typography
            variant="h6"
            noWrap
            component="a"
            href="#"
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            NCSU CAMPUS JOB REVIEW
          </Typography>

          {/* Mobile menu icon */}
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
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
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{ display: { xs: 'block', md: 'none' } }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={() => goto(page)}>
                    <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>

          {/* Main Title for Mobile */}
          <Typography
            variant="h5"
            noWrap
            component="a"
            href="#"
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            NCSU CAMPUS JOB REVIEW
          </Typography>

          {/* Right-aligned buttons (Home and Login) */}
          <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'flex-end' }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={()=>goto(page)}
                sx={{ my: 2, color: 'grey', display: 'block' }}
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
