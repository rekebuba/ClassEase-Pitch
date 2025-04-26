import React, { createContext, useContext, useMemo } from 'react';
import {
    useQueryState,
    useQueryStates,
    parseAsArrayOf,
    parseAsInteger,
    parseAsString,
    parseAsStringEnum,
} from "nuqs";
import { z } from 'zod';
import { getFiltersStateParser, getSortingStateParser } from '@/lib/parsers';

const SearchParamsContext = createContext(null);

export function SearchParamsProvider({ children, columnIds }: { children: React.ReactNode; columnIds: string[] }) {
    // Main search params state
    const [searchParams, setSearchParams] = useQueryStates({
        filterFlag: parseAsStringEnum(["Advanced filters", ""]).withDefault(""),
        page: parseAsInteger.withDefault(1),
        perPage: parseAsInteger.withDefault(10),
        sort: getSortingStateParser().withDefault([{ id: "createdAt", desc: true }]),
        name: parseAsString.withDefault(""),
        grade: parseAsArrayOf(z.number()).withDefault([]),
        section: parseAsArrayOf(z.string()).withDefault([]),
        attendance: parseAsArrayOf(z.coerce.number()).withDefault([]),
        averageGrade: parseAsArrayOf(z.coerce.number()).withDefault([]),
        status: parseAsArrayOf(z.string()).withDefault([]),
        estimatedHours: parseAsArrayOf(z.coerce.number()).withDefault([]),
        createdAt: parseAsArrayOf(z.coerce.number()).withDefault([]),
        filters: getFiltersStateParser(columnIds).withDefault([]),
        joinOperator: parseAsStringEnum(["and", "or"]).withDefault("and"),
    });

    // Individual parameter states with their own setters
    const [filterFlag, setFilterFlag] = useQueryState(
        "filterFlag",
        parseAsStringEnum(["Advanced filters", ""]).withDefault("")
    );

    const [page, setPage] = useQueryState(
        "page",
        parseAsInteger.withDefault(1)
    );

    const [perPage, setPerPage] = useQueryState(
        "perPage",
        parseAsInteger.withDefault(10)
    );

    const [sort, setSort] = useQueryState(
        "sort",
        getSortingStateParser().withDefault([{ id: "createdAt", desc: true }])
    );

    const [name, setName] = useQueryState(
        "name",
        parseAsString.withDefault("")
    );

    const [grade, setGrade] = useQueryState(
        "grade",
        parseAsArrayOf(z.number()).withDefault([])
    );

    const [section, setSection] = useQueryState(
        "section",
        parseAsArrayOf(z.string()).withDefault([])
    );

    const [attendance, setAttendance] = useQueryState(
        "attendance",
        parseAsArrayOf(z.coerce.number()).withDefault([])
    );

    const [averageGrade, setAverageGrade] = useQueryState(
        "averageGrade",
        parseAsArrayOf(z.coerce.number()).withDefault([])
    );

    const [status, setStatus] = useQueryState(
        "status",
        parseAsArrayOf(z.string()).withDefault([])
    );

    const [estimatedHours, setEstimatedHours] = useQueryState(
        "estimatedHours",
        parseAsArrayOf(z.coerce.number()).withDefault([])
    );

    const [createdAt, setCreatedAt] = useQueryState(
        "createdAt",
        parseAsArrayOf(z.coerce.number()).withDefault([])
    );

    const [filters, setFilters] = useQueryState(
        "filters",
        getFiltersStateParser(columnIds).withDefault([])
    );

    const [joinOperator, setJoinOperator] = useQueryState(
        "joinOperator",
        parseAsStringEnum(["and", "or"]).withDefault("and")
    );

    // Utility functions
    const clearAllFilters = () => {
        setSearchParams({
            filterFlag: "",
            page: 1,
            perPage: 10,
            sort: [{ id: "createdAt", desc: true }],
            name: "",
            grade: [],
            section: [],
            attendance: [],
            averageGrade: [],
            status: [],
            estimatedHours: [],
            createdAt: [],
            filters: [],
            joinOperator: "and",
        });
    };

    const getParam = (paramName) => searchParams[paramName];

    const contextValue = useMemo(() => ({
        // All params together
        searchParams,
        setSearchParams,

        // Individual params
        filterFlag, setFilterFlag,
        page, setPage,
        perPage, setPerPage,
        sort, setSort,
        name, setName,
        grade, setGrade,
        section, setSection,
        attendance, setAttendance,
        averageGrade, setAverageGrade,
        status, setStatus,
        estimatedHours, setEstimatedHours,
        createdAt, setCreatedAt,
        filters, setFilters,
        joinOperator, setJoinOperator,

        // Utility functions
        clearAllFilters,
        getParam,
    }), [searchParams, filterFlag, page, perPage, sort, name, grade, section,
        attendance, averageGrade, status, estimatedHours, createdAt, filters, joinOperator]);

    return (
        <SearchParamsContext.Provider value={contextValue}>
            {children}
        </SearchParamsContext.Provider>
    );
}
