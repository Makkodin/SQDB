import React, { useState, useEffect } from "react";
import { Card, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { Input } from 'semantic-ui-react'


function Types() {

    const [ error, setError] = useState(null);
    const [ isLoaded, setIsLoaded] = useState(false);
    const [ types, setTypes ] = useState(null);

    const [ filteredResults, setFilteredResults] = useState(
        ['10X_G', '10X_SC_RNA', '10X_SC_ATAC']
        .sort()
        );

    useEffect(() => {
        fetch(`/types`)
            .then((res) => res.json())
            .then(
                (result) => {
                  setIsLoaded(true);
                  setTypes(result);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, []);

    console.log(filteredResults)

    const searchItems = (searchValue) => {

        if (searchValue) {
            const filterProjects = types.filter((item) => {
                return Object.values(item).join('').toLowerCase().includes(searchValue.toLowerCase())
            })
            setFilteredResults(filterProjects.sort())
        }
        else {setFilteredResults(types.sort())}   
    }

    const slicedArray = filteredResults.slice(0, 10);

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
                    <th>Тип секвенирования</th>
                </tr>
            </thead>
        );
        
        body = (
            <tbody>
                {slicedArray.map((tp, index) => {
                return (
                    <tr key={tp}>
                    <th>{index + 1}</th>
                    <th>
                        <Link to={`/types/${tp}`}>{tp}</Link>
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
        <b>Тип секвенирвания</b><br/><br/>  
        Поиск по типу секвенирования:<br/>
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
export default Types;