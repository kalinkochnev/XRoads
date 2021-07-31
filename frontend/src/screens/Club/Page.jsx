import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import ClubBodyDetail from '../../components/Club/Body/Body';
import Navbar from '../../components/Common/Navbar/Navbar';
import { AutoSlide, Slideshow } from '../../components/Common/Slides/Slides';
import { useStateValue } from '../../service/State';
import * as XroadsAPI from '../../service/xroads-api';


// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubDetail = ({ match: { params } }) => {
  let history = useHistory();
  const [state, dispatch] = useStateValue();

  const [club, setClub] = useState();

  useEffect(() => {
    XroadsAPI.fetchClub(params.clubSlug).then(res => {
      if (res.ok) {
        return res.json().then(clubRes => {
          // console.log(clubRes)
          setClub(clubRes);
        });
      } else {
        history.push(state.school)
      }

    });
  }, [params.clubId]);


  if (club == undefined) {
    return (
      <div>
        <Navbar>xroads</Navbar>
      </div>
    );
  }
  else {
    return (
      <div>
        <Navbar school={params.schoolId}>xroads</Navbar>
        <div className="big">
          <Slideshow>
            {club.slides.map(url => <AutoSlide url={url} />)}
          </Slideshow>
        </div>

        <ClubBodyDetail club={club} />

      </div>
    );
  }
};


export default ScreenClubDetail;
