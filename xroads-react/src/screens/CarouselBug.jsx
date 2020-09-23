import React from "react";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import Carousel, { slidesToShowPlugin } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

const CarouselBug = () => {  
  return (
    <div>
      <div>this is the Caorousel bug:</div>

       

      <div>
        <Carousel>
              <img src='https://brainhubeu.github.io/react-carousel/static/mona-7a1ceae9bdb8c43272eb101c091c5408.jpg' />
                  <img src='https://brainhubeu.github.io/react-carousel/static/scream-ee207a05c1e6fed03aafa156cc511abe.jpg' />
                  <img src='https://brainhubeu.github.io/react-carousel/static/starry-night-39eed0a107ddb6c9f980eb3081a8bdd3.jpg' />
        </Carousel>
      </div>
    </div>
    
  );
};

export default CarouselBug;
