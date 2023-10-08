import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
// import avatar from '../assets/profile.png';
import toast, { Toaster } from 'react-hot-toast';
// import { useFormik } from 'formik';
// import { usernameValidate } from '../helper/validate'
// import { useAuthStore } from '../store/store'
import Webcam from 'react-webcam';
import axios from 'axios';

import styles from '../styles/Username.module.css';

export default function Register() {

  // const navigate = useNavigate();
  // const setUsername = useAuthStore(state => state.setUsername);

  const [cameraActive, setCameraActive] = useState(true); // State to control camera
  const webcamRef = React.useRef(null);


  const handleSubmit = async (e) => {
    e.preventDefault();
    // console.log("handel submit");
    // setCameraActive(false);
    const toastID = toast.loading('Capturing..')
    try {
      const { data } = await axios.post('http://0.0.0.0:2000/attendance');
      // console.log("data.message", data.message); // Print the response data
      if(!data.message){
        return toast.success(`Now ${data.username} is Present !!`,{id: toastID})
      }else{
        return toast.error(`${data.message}`,{id:toastID})
      }
      // setCameraActive(false);

    } catch (error) {
      toast.error("Error to take Attendance",{id:toastID})
      console.error("Error:", error);
    }
  };
  

  useEffect(() => {
    if (!cameraActive) {
      // Access the webcam when the cameraActive state is true
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(stream => {
          if (webcamRef.current) {
            webcamRef.current.srcObject = stream;
          }
        })
        .catch(error => {
          console.error('Error accessing webcam:', error);
        });
    }
  }, [cameraActive]);

  return (
    <div className="container mx-auto">

      <Toaster position='top-center' reverseOrder={false}></Toaster>

      <div className='flex justify-center items-center h-screen'>
        <div className={styles.glass}>

          <div className="title flex flex-col items-center">
            <h4 className='text-5xl font-bold'>Attendance System!</h4>
            {/* <span className='py-4 text-xl w-2/3 text-center text-gray-500'>
              Explore More by connecting with us.
            </span> */}
          </div>

          <div className='py-1'>
            <div className='profile flex justify-center py-4'>
              {cameraActive && <Webcam ref={webcamRef} mirrored={true} width='41%' height={600} />}
            </div>

            <div className="textbox flex flex-col items-center gap-6">
              {/* <input className={styles.textbox} type="text" value={username} name="username" placeholder='Username' onChange={(e)=>{setUsername(e.target.value) ; console.log(username)} }/> */}
              <button className={styles.btn} onClick={handleSubmit}>Make Present</button>
            </div>

            <div className="text-center py-4">
              <span className='text-gray-500'>Not a Member <Link className='text-red-500' to="/register">Register Now</Link></span>
            </div>

          </div>

        </div>
      </div>
    </div>
  )
}
