import './Popup.css'
import  './SpeechLess (2).png';
import  './SpeechLess (1).png';
import SmileIcon from './SmileIcon';
import { useState } from 'react';


export default function Popup(props)
{
  function validateEmail(email) {
    const re = /\S+@\S+\.\S+/;
    return re.test(email);
  }

  let send;
  function signupUser() {
    const firstName = document.querySelector('.signup-first-name').value;
    const lastName = document.querySelector('.signup-last-name').value;
    const email = document.querySelector('.signup-email').value;
    const password = document.querySelector('.signup-password').value;
    const username = document.querySelector('.signup-username').value;
    const how = document.querySelector('.signup-how').selectedOptions[0].value;

    if (!validateEmail(email)) {
      alert('Invalid email');
      return;
    } 
  
 
  
    const newUser = {
      firstName: firstName,
      lastName: lastName,
      email: email,
      password: password,
      username: username,
      how: how
    };
  
    fetch('http://localhost:5000/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newUser)
    })
    .then(response => {
      if (response.ok) {
        // User was successfully signed up
        console.log('User was successfully signed up!');
        send= username+' your successfully signed up!';
        props.onSend(send)
        //send='User was successfully signed up!';
        // Close the signup popup
        ClosePopup();
      } else {
        // There was an error signing up the user
        console.log('Error signing up user');
        // send='Error signing up user';
      }
    })
    .catch(error => {
      console.error('Error signing up user', error);
    });
  }
  
  function authenticateUser() {
    const username = document.querySelector('.signin-username').value;
    const password = document.querySelector('.signin-password').value;
  
    const userCredentials = {
      username: username,
      password: password
    };
    console.log(userCredentials)
    fetch('http://localhost:5000/authenticate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userCredentials)
    })
    .then(response => {
      if (response.ok) {
        // User was successfully authenticated
        console.log('User was successfully authenticated!');
        send= username+' your one of us!';
        props.onSend(send)
        // Close the signin popup
        ClosePopup();
      } else {
        // There was an error authenticating the user
        console.log('Error authenticating user');
      }
    })
    .catch(error => {
      console.error('Error authenticating user', error);
    });
  }



// Define star rating component
const StarRating = () => {

  const starStyles = {
    fontSize: "48px",
    cursor: "pointer",
    display: "inline-block",
    padding: "0 5px",
  
  };
        const [hoverRating, setHoverRating] = useState(0);
        const [selectedRating, setSelectedRating] = useState(0);
      
        // Handle hover event for star divs
        const handleMouseOver = (rating) => {
          setHoverRating(rating);
        };
      
        // Handle mouse leave event for star divs
        const handleMouseLeave = () => {
          setHoverRating(0);
        };
      
        // Handle click event for star divs
        const handleClick = (rating) => {
          setSelectedRating(rating);
        };
      
        return (
          <div>
            {[...Array(5)].map((_, index) => {
              const ratingValue = index + 1;
              return (
                <span
                  key={index}
                  style={ratingValue <= (hoverRating || selectedRating) ? { ...starStyles,color: 'gold' } : { ...starStyles,color: '#ccc' }}
                  onMouseOver={() => handleMouseOver(ratingValue)}
                  onMouseLeave={handleMouseLeave}
                  onClick={() => handleClick(ratingValue)}
                >
                  &#9733;
                </span>
              );
            })}
          </div>
        );
       };


                    
function ClosePopup()
{
        document.querySelector('.popup1').classList.remove('popupActive1');
        document.querySelector('.popup2').classList.remove('popupActive1');
        document.querySelector('.popup').classList.add('popupunActive');
}
function OpenPopupSignin()
{
        document.querySelector('.popup1').classList.add('popupActive1');
}
function OpenPopupConnect()
{
        document.querySelector('.popup2').classList.add('popupActive1');
}



return(
        <>
<div className="popup">
<div>
<img src={require('./SpeechLess (1).png')} alt="SpeechLess" style={{ width: '350px',height: 'auto',position:'absolute',top:'0px',left: '170px'}} />
<div className="a">
<h1>Wolcome to SpeechLess!</h1>
<h2>We are glad to see you here</h2>
<h4>We wish you a pleasant that will leave you speechless<SmileIcon/></h4>
<br/>
<button onClick={()=>OpenPopupSignin()} style={{width:'250px'}}>Sign Up</button>
<br/>
<button onClick={()=>OpenPopupConnect()} style={{width:'250px'}}>Sign In</button>
</div>
</div>
</div>


<div class="popup1">
<div>
<img src={require('./SpeechLess (1).png')} alt="SpeechLess" style={{ width: '350px',height: 'auto',position:'absolute',top:'0px',left: '170px'}} />
<div className="ab">

<div className="b">
<h5>Enter your first name:</h5>
<input type={'text'} class="signup-first-name"/>
<h5>Enter your last name:</h5>
<input type={'text'} class="signup-last-name"/>
<h5>Enter your Email:</h5>
<input type={'text'} class="signup-email"/>
</div>
<div className="c">
<h5>Choose your password:</h5>
<input type={'text'} class="signup-password"/>
<h5>Choose your yoser name:</h5>
<input type={'text'} class="signup-username"/>
<h5>How do hear about us:</h5>
<select style={{width:'200px',height:'26px',margin:'2px'}} class="signup-how">
        <option>enternet</option>
        <option>family</option>
        <option>friends</option>
</select>
</div>
</div>
<h1></h1>
<button onClick={()=>signupUser()} style={{width:'150px',height:'50px',margin:'50px auto '}}>Get in</button>
</div>
</div>


<div className="popup2">
<div>
<img src={require('./SpeechLess (1).png')} alt="SpeechLess" style={{ width: '350px',height: 'auto',position:'absolute',top:'0px',left: '170px'}} />
<div className="a">
<div className="d">
<h5>User name:</h5>
<input type={'text'} style={{width:'250px'}} class="signin-username"/>
<h5>Password:</h5>
<input type={'text'} style={{width:'250px'}} class="signin-password"/>
</div>
<h3>Rate your user experience</h3>
<div style={{margin:'auto'}}><StarRating style={{width:'60px'}}/></div>
<br/>
<br/>
<button onClick={()=>authenticateUser()} style={{width:'200px'}}>Get in</button>
</div>
</div>
</div>

</>);
}
