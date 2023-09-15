import React, { useState, useEffect } from "react";
import { Card, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Input } from 'semantic-ui-react'


function Projects() {

    // Блок отрисовки
    const [ error, setError] = useState(null);
    const [ isLoaded, setIsLoaded] = useState(false);
    const [ projects, setProjects ] = useState(null);

    // Блок поиска
    // Пришлось сделать костыль со списком данных (в первый раз рендерится без него)
    //const [ searchInput, setSearchInput] = useState("");
    const [ filteredResults, setFilteredResults] = useState(
        ['M', 'ONC_INH', 'CSP', 'G', 'RONC_3', 'RONC-1-GISO', 'RONC-3', 'ONC_R']
        .sort()
        );

    // Подгрузка данных по именам проектов из flask
    useEffect(() => {
        fetch(`/projects`)
            .then((res) => res.json())
            .then(
                (result) => {
                  setIsLoaded(true);
                  setProjects(result);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, []);// eslint-disable-line react-hooks/exhaustive-deps
    
    
    console.log(filteredResults)

    const searchItems = (searchValue) => {

        if (searchValue) {
            //setSearchInput(searchValue)
            const filterProjects = projects.filter((item) => {
                return Object.values(item).join('').toLowerCase().includes(searchValue.toLowerCase())
            })
            setFilteredResults(filterProjects.sort())
        }
        else {setFilteredResults(projects.sort())}   
    }

    const slicedArray = filteredResults.slice(0, 10);

    // Отрисовка блоков
    let body = <></>;
    let head = <></>;
    let search = <></>;

    if (error) {
        return <div>Ошибка: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Загрузка...</div>;
    } else {
        head = (
            <thead>
                <tr>
                    <th>№</th>
                    <th>Проект</th>
                </tr>
            </thead>
        );
        
        body = (
            <tbody>
                {slicedArray.map((prj, index) => {
                return (
                    <tr key={prj}>
                    <th>{index + 1}</th>
                    <th>
                        <Link to={`/projects/${prj}`}>{prj}</Link>
                    </th>
                    </tr>
                );
                })}
            </tbody>
        );

        search = (     
            <Input icon="search" placeholder='Поиск...' type="text" onChange={(e) => searchItems(e.target.value)}/>
        );
    }

    return (
        <><hr/>
        <Card>
        <b>Проекты</b><br/><br/>  
        Поиск по проектам:<br/>
        {search}
        <br/>
        </Card>    
        <hr/>


        <Card>
        <Table bordered hover>
            {head}
            {body}
        </Table>
        </Card>

        <hr/>
        </>
    );
}
export default Projects;