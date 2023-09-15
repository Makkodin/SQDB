/* eslint-disable jsx-a11y/alt-text */
import React from "react";
import {
    MDBCard,
    MDBCardBody,
    MDBCardTitle,
    MDBCardText
  } from 'mdb-react-ui-kit';
//import logo from "./../image/logo.png"

import "./../styles/Home.css"

function Home() {
    return (
        <MDBCard className="main-page">
            <MDBCardBody>
                <MDBCardTitle>
                <a>SQDB: Sequence Database</a>
                </MDBCardTitle>

                <MDBCardText>
                <b>
                Добро пожаловать в сервис ЦСП созданный для поиска
                и анализа результатов (наличие, качество, принадлежность)
                секвенирования.
                </b>
                </MDBCardText>
            
                <MDBCardText>
                <b>
                Для навигации по сервису можно используйте значек расположеный
                в верхнем правом углу. 
                </b>
                </MDBCardText>

                <MDBCardText>
                ***Тут будет Таблица с 4 столбцами 1) Типы секвенирования 2) Количество батчей 
                3) Количество ячеек 4) количество образцов **
                </MDBCardText>

            </MDBCardBody>
        </MDBCard>
      );
}

export default Home;


//<>
//<Card>
//    <div className="home-page"><br/>
//    
//    Добро пожаловать в систему поиска результатов секвенирования SQDB!<br/>    
//    Для навигации используйте кнопки в заголовке.<br/><br/>
//    Проекты - список всех проектов<br/>
//    Ячейки - список всех ячеек<br/>
//    Биообразцы - список всех биообразцов<br/><br/>
//    
//</div>
//</Card>
//</>
            