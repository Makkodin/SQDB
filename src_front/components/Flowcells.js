import React, { useState, useEffect } from "react";
import { Card, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Input } from 'semantic-ui-react'


function Flowcells() {

    // Блок отрисовки
    const [ error, setError] = useState(null);
    const [ isLoaded, setIsLoaded] = useState(false);
    const [ flowcells, setFlowcells ] = useState(null);

    // Блок поиска
    // Пришлось сделать костыль со списком данных (в первый раз рендерится без него)
    //const [ searchInput, setSearchInput] = useState("");
    const [ filteredResults, setFilteredResults] = useState(
        ["200629_A00919_0083_AH23J2DSXY",
        "200720_A01013_0095_AH7KFCDSXY",
        "200723_A01013_0097_AH2522DSXY",
        "200918_A00964_0074_BH7K3HDSXY",
        "201001_A00923_0127_AH7KH2DSXY",
        "201020_A00919_0129_BH7K3CDSXY"]
        .sort()
        );

    // Подгрузка данных по именам проектов из flask
    useEffect(() => {
        fetch(`/flowcells`)
            .then((res) => res.json())
            .then(
                (result) => {
                  setIsLoaded(true);
                  setFlowcells(result);
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
            const filterProjects = flowcells.filter((item) => {
                return Object.values(item).join('').toLowerCase().includes(searchValue.toLowerCase())
            })
            setFilteredResults(filterProjects.sort())
        }
        else {setFilteredResults(flowcells.sort())}   
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
                    <th>Ячейка</th>
                </tr>
            </thead>
        );
        
        body = (
            <tbody>
                {slicedArray.map((id, index) => {
                return (
                    <tr key={id}>
                    <th>{index + 1}</th>
                    <th>
                        <Link to={`/flowcells/${id}`}>{id}</Link>
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
export default Flowcells;